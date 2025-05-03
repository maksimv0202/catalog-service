import asyncio
import functools
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI

from core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    try:
        await asyncio.to_thread(functools.partial(command.upgrade, Config('alembic.ini'), 'head'))
        print('Upgrade alembic migrations to HEAD')
    except Exception as e:
        print(f'An error while upgrading alembic migrations: {e}')
        raise
    yield
