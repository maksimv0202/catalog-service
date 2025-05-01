from abc import ABCMeta, abstractmethod
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.base import Base


type _T_model = Base


class BaseRepository(metaclass=ABCMeta):

    @abstractmethod
    async def get(self, pk: int) -> _T_model | None:
        pass

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> list[_T_model]:
        pass

    @abstractmethod
    async def create(self, data: dict) -> _T_model:
        pass

    @abstractmethod
    async def delete(self, pk: int) -> _T_model:
        pass

    @abstractmethod
    async def filter(self, **filters) -> list[_T_model]:
        pass


class GenericRepository[_T_model](BaseRepository):

    def __init__(self, model: Type[_T_model], session: AsyncSession):
        self._model = model
        self._session = session

    async def get(self, pk: int) -> _T_model | None:
        return await self._session.get(self._model, pk)

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[_T_model]:
        query = select(self._model).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def create(self, data: dict) -> _T_model:
        instance = self._model(**data)
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance

    async def delete(self, pk: int) -> _T_model:
        instance = await self.get(pk)
        await self._session.delete(instance)
        await self._session.commit()
        return instance

    async def filter(self, **filters) -> list[_T_model]:
        query = select(self._model)
        if filters:
            query = query.filter_by(**filters)
        return list(await self._session.scalars(query))
