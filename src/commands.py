import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from core.db import engine
from core.repositories.activity import ActivityRepository
from core.repositories.building import BuildingRepository
from core.repositories.organization import OrganizationRepository


ACTIVITIES = [
    {
        'name': 'Еда',
        'children': [
            {'name': 'Мясная продукция'},
            {'name': 'Молочная продукция'}
        ]
    },
    {
        'name': 'Автомобили',
        'children': [
            {'name': 'Грузовые'},
            {
                'name': 'Легковые',
                'children': [
                    {'name': 'Запчасти'},
                    {'name': 'Аксесуары'}
                ]
            }
        ]
    }
]

BUILDINGS = [
    {
        'address': '4-й Добрынинский переулок, 1/9с1, Москва, 119049',
        'latitude': 55.724261,
        'longitude': 37.617249
    },
    {
        'address': 'Советская улица, 4, Балашиха, Московская область, 143912',
        'latitude': 55.796122,
        'longitude': 37.934983
    },
    {
        'address': 'улица Маршала Катукова, 6к2, Москва, 123592',
        'latitude': 55.809125,
        'longitude': 37.400387
    },
    {
        'address': 'Новочеркасский бульвар, 51, Москва, 109369',
        'latitude': 55.648413,
        'longitude': 37.739519
    },
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
        'activity_id': 2,
    },
    {
        'name': 'Молочный Мир',
        'phone_number': '+74959876543',
        'building_id': 2,
        'activity_id': 3,
    },
    {
        'name': 'АвтоГруз',
        'phone_number': '+74952223344',
        'building_id': 1,
        'activity_id': 4,
    },
    {
        'name': 'Все для авто',
        'phone_number': '+74951112233',
        'building_id': 1,
        'activity_id': 6,
    },
]


async def create_activities_recursive(
    data: list[dict],
    repository: ActivityRepository,
    parent_id: int | None = None
):
    for node in data:
        if await repository.exists(name=node['name']):
            continue
        _c_node = await repository.create({'name': node['name'], 'parent_id': parent_id})
        if 'children' in node:
            await create_activities_recursive(node['children'], repository, parent_id=_c_node.id)


async def create_buildings(data: list[dict], repository: BuildingRepository):
    for _b in data:
        await repository.create(_b)


async def create_organizations(data: list[dict], repository: OrganizationRepository):
    for _o in data:
        await repository.create(_o)


async def generate_data():
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        try:
            await create_activities_recursive(ACTIVITIES, ActivityRepository(session), None)
        except Exception as exc:
            print('An error while create activities:', exc)
        print('CREATE ACTIVITIES RECURSIVE: OK')

        try:
            await create_buildings(BUILDINGS, BuildingRepository(session))
        except Exception as exc:
            print('An error while create buildings:', exc)
        print('CREATE BUILDINGS: OK')

        try:
            await create_organizations(ORGANIZATIONS, OrganizationRepository(session))
        except Exception as exc:
            print('An error while create organizations:', exc)
        print('CREATE ORGANIZATIONS: OK')
    await engine.dispose()


if __name__ == '__main__':
    EXECUTABLE = {
        'generate_data': generate_data
    }
    if len(sys.argv) != 2:
        sys.exit(1)
    _exec = EXECUTABLE[sys.argv[1]]
    try:
        asyncio.run(_exec())
    except Exception as e:
        print(e)
