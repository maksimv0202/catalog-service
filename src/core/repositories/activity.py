from collections.abc import Sequence
from sqlalchemy import select, delete, update, func, Integer
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ExceededMaxDepthError
from core.models import Activity
from core.repositories.base import GenericRepository


class ActivityRepository(GenericRepository[Activity]):

    MAX_DEPTH = 3

    def __init__(self, session: AsyncSession):
        super().__init__(Activity, session)

    async def get_by_name(self, name: str) -> Activity:
        return (await self._session.execute(
            select(Activity).where(Activity.id == name)
        )).scalar_one_or_none()

    async def create(self, data: dict) -> Activity:
        parent_id: int = data.get('parent_id')
        if parent_id is not None:
            depth = await self.get_nested_depth(parent_id)
            if depth >= self.MAX_DEPTH:
                raise ExceededMaxDepthError('The maximum allowed nesting level has been exceeded')
        instance = self._model(**data)
        self._session.add(instance)
        try:
            await self._session.commit()
            await self._session.refresh(instance)
            return instance
        except Exception:
            await self._session.rollback()
            raise

    async def update(self, pk: int, data: dict) -> Activity:
        new_parent_id = data.get('parent_id')
        if new_parent_id is not None:
            depth = await self.get_nested_depth(new_parent_id)
            subtree_depth = await self.get_subtree_max_depth(pk)
            if depth + subtree_depth > self.MAX_DEPTH:
                raise ExceededMaxDepthError('The maximum allowed nesting level has been exceeded')
        result = await self._session.execute(
            update(self._model)
            .where(self._model.id == pk)  # type: ignore
            .values(**data)
            .returning(self._model)
        )
        await self._session.commit()
        return result.scalar_one()

    async def get_nested_depth(self, parent_id: int) -> int:
        depth = 1
        _p_id = parent_id

        while _p_id:
            parent_id = await self._session.scalar(
                select(Activity.parent_id)
                .where(Activity.id == _p_id)
            )
            if parent_id:
                depth += 1
            _p_id = parent_id
        return depth

    async def get_subtree_max_depth(self, root_id: int) -> int:
        subtree = (
            select(
                self._model.id.label('id'),
                self._model.parent_id.label('parent_id'),
                func.cast(1, Integer).label('depth'),
            )
            .where(self._model.id == root_id)
            .cte(recursive=True)
        )
        subtree = subtree.union_all(
            select(
                self._model.id,
                self._model.parent_id,
                (subtree.c.depth + 1).label('depth'),
            ).where(self._model.parent_id == subtree.c.id)
        )
        max_depth = await self._session.scalar(
            select(func.max(subtree.c.depth))
        )
        return max_depth or 0

    async def get_roots(self) -> Sequence[Activity]:
        return (await self._session.scalars(
            select(Activity)
            .where(Activity.parent_id.is_(None)))
        ).all()

    async def delete_with_children(self, activity_id: int) -> None:
        subtree = (
            select(Activity.id)
            .where(Activity.id == activity_id)
            .cte(name='subtree', recursive=True)
        )
        subtree = subtree.union_all(
            select(Activity.id)
            .where(Activity.parent_id == subtree.c.id)
        )
        await self._session.execute(
            select(Activity.id)
            .where(Activity.id.in_(select(subtree.c.id)))
            .with_for_update(nowait=True)
        )
        await self._session.execute(
            delete(Activity)
            .where(Activity.id.in_(select(subtree.c.id)))
        )
        await self._session.commit()
