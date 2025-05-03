from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.db import get_async_session
from core.repositories.building import BuildingRepository
from core.schemas.building import BuildingCreate, BuildingOut, BuildingUpdate
from core.schemas.pagination import PageParams

router = APIRouter()


@router.get('', response_model=list[BuildingOut], status_code=status.HTTP_200_OK)
async def get_buildings(
    page_params: PageParams = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    return await BuildingRepository(session).get_all(
        limit=page_params.limit, offset=page_params.page - 1
    )


@router.get('/{building_id}', response_model=BuildingOut, status_code=status.HTTP_200_OK)
async def get_building_by_id(
    building_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    building = await BuildingRepository(session).get(building_id)
    if building is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return building


@router.post('', response_model=BuildingOut, status_code=status.HTTP_201_CREATED)
async def create_building(
    data: BuildingCreate,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        return await BuildingRepository(session).create(data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.delete('/{building_id}', response_model=BuildingOut, status_code=status.HTTP_200_OK)
async def delete_building(
    building_id: int,
    session: AsyncSession = Depends(get_async_session)
):
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
async def update_building(
    building_id: int,
    data: BuildingUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    repository = BuildingRepository(session)
    building = await repository.get(building_id)
    if building is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    try:
        return await repository.update(building_id, data.model_dump(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
