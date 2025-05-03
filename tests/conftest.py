from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from core.config import settings
from core.db import get_async_session
from core.models import Base
from main import app


@pytest_asyncio.fixture(scope='function', loop_scope='function')
async def async_engine():
    engine = create_async_engine('postgresql+asyncpg://{}:{}@{}:{}/{}'.format(
        settings.POSTGRES_USERNAME,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
        settings.POSTGRES_PORT,
        settings.POSTGRES_DB),
        poolclass=StaticPool,
        echo=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_session(async_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(async_engine, class_=AsyncSession,
                                       autoflush=False, future=True, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def async_client(async_session) -> AsyncGenerator[AsyncClient, None]:

    async def override_get_async_session():
        yield async_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://127.0.0.1:8000/api/v1/',
        headers={'X-API-KEY': settings.SECRET_KEY, 'Content-Type': 'application/json'}
    ) as client:
        yield client
