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

    get_result = await repository.get(1)
    assert get_result.address == data['address']


@pytest.mark.asyncio
async def test_delete_building_by_id(async_session):
    repository = BuildingRepository(async_session)
    data = BUILDINGS[0]
    await repository.create(data)
    assert len(await repository.get_all()) == 1
    await repository.delete(1)
    assert len(await repository.get_all()) == 0


@pytest.mark.asyncio
async def test_update_building_by_id(async_session):
    repository = BuildingRepository(async_session)
    data = BUILDINGS[0]
    await repository.create(data)
    update_result = await repository.update(1, {'address': 'updated', 'latitude': 1, 'longitude': 2})
    assert update_result.address == 'updated'
    assert update_result.latitude == 1
    assert update_result.longitude == 2

    get_result = await repository.get(1)
    assert get_result.address == 'updated'
    assert get_result.latitude == 1
    assert get_result.longitude == 2


@pytest.mark.asyncio
async def test_filter_building_by_fields(async_session):
    repository = BuildingRepository(async_session)
    data = BUILDINGS[:2]
    for building in data:
        await repository.create(building)

    filter_1_result = await repository.filter(address=data[0]['address'])
    assert len(filter_1_result) != 0
    assert filter_1_result[0].address == data[0]['address']
