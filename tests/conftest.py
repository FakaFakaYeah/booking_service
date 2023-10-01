import asyncio

import pytest

from app.core import Base, settings
from app.core.db import engine, async_session_maker

pytest_plugins = [
    'tests.fixtures.users',
    'tests.fixtures.data'
]


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST', (
        "Для тестирования укажите mode = TEST"
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def session():
    async with async_session_maker() as session:
        yield session

