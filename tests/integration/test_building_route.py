import pytest
from starlette import status


@pytest.mark.asyncio
async def test_create_building(async_client):
    payload = {
        'address': 'шоссе Энтузиастов, 50, Москва, 111123',
        'latitude': 55.759203,
        'longitude': 37.758743
    }
    response = await async_client.post('/buildings', json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['address'] == payload['address']
    assert response.json()['latitude'] == payload['latitude']
    assert response.json()['longitude'] == payload['longitude']


@pytest.mark.asyncio
async def test_get_empty_buildings(async_client):
    response = await async_client.get('/buildings')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_building_by_id_not_found(async_client):
    response = await async_client.get('/buildings/1')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_building_by_id_not_found(async_client):
    response = await async_client.patch('/buildings/1', json={})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_building_by_id_not_found(async_client):
    response = await async_client.delete('/buildings/1')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_buildings(async_client, async_session):
    payload = {
        'address': 'шоссе Энтузиастов, 50, Москва, 111123',
        'latitude': 55.759203,
        'longitude': 37.758743
    }
    r = await async_client.post('/buildings', json=payload)

    response = await async_client.get('/buildings', params={'page': 1, 'limit': 100})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() != []
