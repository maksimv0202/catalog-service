from abc import ABCMeta, abstractmethod
from collections.abc import Sequence
from typing import Type

from sqlalchemy import exists, select, update, and_, between
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from core.models.base import Base


type _T_model = Base


class BaseRepository(metaclass=ABCMeta):

    @abstractmethod
    async def get(self, pk: int) -> _T_model | None:
        pass

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> Sequence[_T_model]:
        pass

    @abstractmethod
    async def create(self, data: dict) -> _T_model:
        pass

    @abstractmethod
    async def delete(self, pk: int) -> _T_model:
        pass

    @abstractmethod
    async def filter(self, limit: int, offset: int, **filters) -> Sequence[_T_model]:
        pass


class GenericRepository[_T_model](BaseRepository):

    __slots__ = ('_model', '_session')

    def __init__(self, model: Type[_T_model], session: AsyncSession):
        self._model = model
        self._session = session

    async def get(self, pk: int) -> _T_model | None:
        return await self._session.get(self._model, pk)

    async def get_all(self, limit: int = 100, offset: int = 0) -> Sequence[_T_model]:
        return (await self._session.scalars(
            select(self._model)
            .limit(limit)
            .offset(offset)
        )).all()

    async def create(self, data: dict) -> _T_model:
        instance = self._model(**data)
        self._session.add(instance)
        try:
            await self._session.commit()
            await self._session.refresh(instance)
            return instance
        except Exception:
            await self._session.rollback()
            raise

    async def delete(self, pk: int) -> _T_model:
        instance = await self.get(pk)
        await self._session.delete(instance)
        await self._session.commit()
        return instance

    async def update(self, pk: int, data: dict) -> _T_model:
        result = await self._session.execute(
            update(self._model)
            .where(self._model.id == pk)  # type: ignore
            .values(**data)
            .returning(self._model)
        )
        await self._session.commit()
        return result.scalar_one()

    async def exists(self, pk: int | None = None, **unique_fields) -> bool:
        if pk is not None:
            condition = self._model.id == pk
        elif unique_fields:
            condition = and_(getattr(self._model, field) == value
                             for field, value in unique_fields.items())
        else:
            raise ValueError()
        return await self._session.scalar(
            select(exists().where(condition))  # type: ignore
        )

    async def filter(self, limit: int = 100, offset: int = 0, **filters) -> Sequence[_T_model]:
        query = select(self._model)
        conditions = []
        joins = {}
        for key, val in filters.items():
            if '__' in key:
                relation, field_op = key.split('__', 1)
                if relation not in joins:
                    related_model = getattr(self._model, relation).property.mapper.class_
                    joins[relation] = aliased(related_model)
                    query = query.join(joins[relation], getattr(self._model, relation))
                model_field = getattr(joins[relation], field_op.replace('__in', ''))
                if field_op.endswith('__in') and isinstance(val, tuple) and len(val) == 2:
                    conditions.append(between(model_field, val[0], val[1]))
                else:
                    conditions.append(model_field == val)
            else:
                model_field = getattr(self._model, key)
                conditions.append(model_field == val)
        if conditions:
            query = query.where(and_(*conditions))
        return (await self._session.scalars(
            query.limit(limit).offset(offset)
        )).all()
