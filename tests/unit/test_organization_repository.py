import pytest

from core.repositories.activity import ActivityRepository
from core.repositories.building import BuildingRepository
from core.repositories.organization import OrganizationRepository

ACTIVITIES = [
    {'name': 'Еда'},
    {'name': 'Мясная продукция', 'parent_id': 1},
]

BUILDINGS = [
    {
        'address': 'шоссе Энтузиастов, 50, Москва, 111123',
        'latitude': 55.759203,
        'longitude': 37.758743
    },
]

ORGANIZATIONS = [
    {
        'name': 'Мясной Дом',
        'phone_number': '+74951234567',
        'building_id': 1,
        'activity_id': 1,
    },
]


@pytest.mark.asyncio
async def test_create_organization(async_session):
    activity = ACTIVITIES[0]
    building = BUILDINGS[0]
    organization = ORGANIZATIONS[0]
    await ActivityRepository(async_session).create(activity)
    await BuildingRepository(async_session).create(building)
    repository = OrganizationRepository(async_session)
    result = await repository.create(organization)
    assert result.id == 1
    assert result.name == organization['name']
    assert result.phone_number == organization['phone_number']
    assert result.building_id == organization['building_id']
    assert result.activity_id == organization['activity_id']
