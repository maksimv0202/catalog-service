from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.db import get_async_session
from core.repositories.activity import ActivityRepository
from core.repositories.building import BuildingRepository
from core.repositories.organization import OrganizationRepository
from core.schemas.organization import OrganizationOut, OrganizationCreate, OrganizationUpdate
from core.schemas.pagination import PageParams
from core.services.organization import OrganizationService

router = APIRouter()


@router.get('', response_model=list[OrganizationOut], status_code=status.HTTP_200_OK)
async def get_organizations(
    name: str | None = Query(default=None, description='Filter by Organization name'),
    building_id: int | None = Query(default=None, description='Filter by Building ID'),
    activity_id: int | None = Query(default=None, description='Filter by Activity ID'),
    page_params: PageParams = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    filters = {}
    if name:
        filters['name'] = name
    if building_id:
        filters['building_id'] = building_id
    if activity_id:
        filters['activity_id'] = activity_id
    return await OrganizationRepository(session).filter(
        limit=page_params.limit,
        offset=page_params.page - 1,
        **filters
    )


@router.get('/search', response_model=list[OrganizationOut], status_code=status.HTTP_200_OK)
async def search_organizations(
    activity: str = Query(default=None, description=''),
    session: AsyncSession = Depends(get_async_session)
):
    return await OrganizationRepository(session).search_by_activity_name(activity)


@router.get('/search/by-radius', response_model=list[OrganizationOut], status_code=status.HTTP_200_OK)
async def search_organizations_by_search_point_and_radius(
    point: str = Query(..., description='Coordinates of the point in the format `lat, lon`'),
    radius: int = Query(..., description='Search radius in meters'),
    page_params: PageParams = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    lat, lon = map(lambda t: float(t.strip()), point.split(','))
    print(lat, lon)
    service = OrganizationService(OrganizationRepository(session))
    return await service.search_by_radius(
        lat, lon, radius, page_params.limit, page_params.page - 1
    )


@router.get('/search/by-area', response_model=list[OrganizationOut], status_code=status.HTTP_200_OK)
async def search_organizations_by_rectangular_area(
    point1: str = Query(..., description='Coordinates of the first point of the rectangle in the format `lat, lon`'),
    point2: str = Query(..., description='Coordinates of the second point of the rectangle in the format `lat, lon`'),
    page_params: PageParams = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    lat1, lon1 = map(lambda t: float(t.strip()), point1.split(','))
    lat2, lon2 = map(lambda t: float(t.strip()), point2.split(','))
    service = OrganizationService(OrganizationRepository(session))
    return await service.search_by_area(
        lat1, lon1, lat2, lon2, page_params.limit, page_params.page - 1
    )


@router.get('/{organization_id}', response_model=OrganizationOut, status_code=status.HTTP_200_OK)
async def get_organization_by_id(
    organization_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    organization = await OrganizationRepository(session).get(organization_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return organization


@router.post('', response_model=OrganizationOut, status_code=status.HTTP_201_CREATED)
async def create_organization(
    data: OrganizationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repository = OrganizationRepository(session)
    if await repository.exists(name=data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Organization with name `{data.name}` already exists'
        )
    if not await BuildingRepository(session).exists(data.building_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Building `{data.building_id}` not found'
        )
    if not await ActivityRepository(session).exists(data.activity_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Activity `{data.activity_id}` not found'
        )
    instance = await repository.create(data.model_dump())
    await session.refresh(instance, ['building', 'activity'])
    return instance


@router.patch('/{organization_id}', response_model=OrganizationOut, status_code=status.HTTP_200_OK)
async def update_organization(
    organization_id: int,
    data: OrganizationUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    repository = OrganizationRepository(session)
    if await repository.exists(name=data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Organization with name `{data.name}` already exists'
        )
    if not await BuildingRepository(session).exists(data.building_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Building `{data.building_id}` not found'
        )
    if not await ActivityRepository(session).exists(data.activity_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Activity `{data.activity_id}` not found'
        )
    try:
        return await repository.update(organization_id, data.model_dump(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.delete('/{organization_id}', response_model=OrganizationOut, status_code=status.HTTP_200_OK)
async def delete_organization(
    organization_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repository = OrganizationRepository(session)
    organization = await repository.get(organization_id)
    if organization is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    try:
        await repository.delete(organization_id)
        return organization
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
