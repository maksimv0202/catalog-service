from collections.abc import Sequence
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Activity
from core.repositories.base import GenericRepository


class ActivityRepository(GenericRepository[Activity]):

    def __init__(self, session: AsyncSession):
        super().__init__(Activity, session)

    async def get_by_name(self, name: str) -> Activity:
        return (await self._session.execute(
            select(Activity).where(Activity.id == name)
        )).scalar_one_or_none()

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

    async def get_roots(self) -> Sequence[Activity]:
        return (await self._session.execute(
            select(Activity)
            .where(Activity.parent_id.is_(None)))
        ).scalars().all()

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
