import pytest

from core.repositories.building import BuildingRepository


BUILDINGS = [
    {
        'address': 'шоссе Энтузиастов, 50, Москва, 111123',
        'latitude': 55.759203,
        'longitude': 37.758743
    },
    {
        'address': 'Новочеркасский бульвар, 51, Москва, 109369',
        'latitude': 55.648413,
        'longitude': 37.739519
    }
]


@pytest.mark.asyncio
async def test_create_building(async_session):
    data = BUILDINGS[0]
    result = await BuildingRepository(async_session).create(data)
    assert result.id == 1
    assert result.address == data['address']
    assert result.latitude == data['latitude']
    assert result.longitude == data['longitude']


@pytest.mark.asyncio
async def test_get_empty_building(async_session):
    result = await BuildingRepository(async_session).get(1)
    assert result is None


@pytest.mark.asyncio
async def test_get_all_buildings(async_session):
    repository = BuildingRepository(async_session)
    data = BUILDINGS[:2]
    for building in data:
        await repository.create(building)

    result = await repository.get_all()
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_building_by_id(async_session):
    repository = BuildingRepository(async_session)
    data = BUILDINGS[0]
    await repository.create(data)

    result = await repository.exists(1)
    assert result is True
