from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.db import get_async_session
from core.repositories.activity import ActivityRepository
from core.schemas.activity import ActivityOut, ActivityCreate, ActivityUpdate
from core.schemas.pagination import PageParams

router = APIRouter()


@router.get('', response_model=list[ActivityOut], status_code=status.HTTP_200_OK)
async def get_activities(
    page_params: PageParams = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    return await ActivityRepository(session).get_all(
        limit=page_params.limit, offset=page_params.page - 1
    )


@router.post('', response_model=ActivityOut, status_code=status.HTTP_201_CREATED)
async def create_activity(
    data: ActivityCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repository = ActivityRepository(session)
    if await repository.exists(name=data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Acivity with name `{data.name}` already exists'
        )
    if data.parent_id is not None:
        depth = await repository.get_nested_depth(data.parent_id)
        if depth >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The maximum allowed nesting level has been exceeded',
            )
    return await repository.create(data.model_dump())


@router.get('/{activity_id}', response_model=ActivityOut, status_code=status.HTTP_200_OK)
async def get_activity_by_id(
    activity_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return await ActivityRepository(session).get(activity_id)


@router.patch('/{activity_id}', response_model=ActivityOut, status_code=status.HTTP_200_OK)
async def update_activity(
    activity_id: int,
    data: ActivityUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    repository = ActivityRepository(session)
    if not await repository.exists(activity_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    if data.parent_id is not None:
        depth = await repository.get_nested_depth(data.parent_id)
        if depth >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The maximum allowed nesting level has been exceeded',
            )
    return await repository.update(activity_id, data.model_dump())


@router.delete('/{activity_id}', response_model=ActivityOut, status_code=status.HTTP_200_OK)
async def delete_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repository = ActivityRepository(session)
    root = await repository.get(activity_id)
    if root is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    await repository.delete_with_children(activity_id)
    return root
