import pytest

from core.exceptions import ExceededMaxDepthError
from core.repositories.activity import ActivityRepository

ACTIVITIES = [
    {'name': 'Еда'},
    {'name': 'Мясная продукция', 'parent_id': 1},
    {'name': 'Молочная продукция', 'parent_id': 1}
]


@pytest.mark.asyncio
async def test_create_single_activity(async_session):
    data = ACTIVITIES[0]
    result = await ActivityRepository(async_session).create(data)
    assert result.id == 1
    assert result.name == data['name']
    assert result.parent_id is None


@pytest.mark.asyncio
async def test_create_activity_with_children(async_session):
    repository = ActivityRepository(async_session)
    data = ACTIVITIES
    for activity in data:
        await repository.create(activity)
    assert (await repository.get_roots())[0].name == data[0]['name']
    assert len(await repository.get_all()) == 3


@pytest.mark.asyncio
async def test_create_max_depth_activities(async_session):
    repository = ActivityRepository(async_session)
    data = ACTIVITIES
    for activity in data:
        await repository.create(activity)
    await repository.create({'name': '1', 'parent_id': 2})
    await repository.create({'name': '2', 'parent_id': 3})
    with pytest.raises(ExceededMaxDepthError) as e:
        await repository.create({'name': '3', 'parent_id': 4})
