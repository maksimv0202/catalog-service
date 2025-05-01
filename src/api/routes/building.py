from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.db import get_async_session
from core.repositories.building import BuildingRepository
from core.schemas.building import BuildingCreate, BuildingOut, BuildingUpdate

router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_buildings(session: AsyncSession = Depends(get_async_session)):
    buildings = await BuildingRepository(session).get_all()
    return buildings


@router.post('/', response_model=BuildingOut, status_code=status.HTTP_201_CREATED)
async def create_building(data: BuildingCreate, session: AsyncSession = Depends(get_async_session)):
    building = await BuildingRepository(session).create(data.model_dump())
    return building


@router.delete('/{building_id}', response_model=BuildingOut, status_code=status.HTTP_200_OK)
async def delete_building(building_id: int, session: AsyncSession = Depends(get_async_session)):
    repository = BuildingRepository(session)
    building = await repository.get(building_id)
    if building is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    try:
        await repository.delete(building_id)
        return building
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.patch('/{building_id}', response_model=BuildingUpdate, status_code=status.HTTP_200_OK)
async def update_building(building_id: int, data: BuildingUpdate, session: AsyncSession = Depends(get_async_session)):
    repository = BuildingRepository(session)
    building = await repository.get(building_id)
    if building is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    try:
        updated = await repository.update(building_id, data.model_dump(exclude_unset=True))
        return updated
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
