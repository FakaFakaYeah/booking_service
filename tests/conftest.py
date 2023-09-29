import asyncio

import pytest
from httpx import AsyncClient

from app.core import Base
from app.core import settings
from app.core.db import engine, async_session_maker
from app.main import app as fast_api_app

pytest_plugins = [
    'tests.fixtures.users'
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


@pytest.fixture
async def session():
    async with async_session_maker() as session:
        yield session


@pytest.fixture
async def test_client():
    async with AsyncClient(app=fast_api_app, base_url='http://test') as client:
        yield client


@pytest.fixture(scope='session')
async def get_cookie():

    async with AsyncClient(app=fast_api_app, base_url='http://test') as client:
        email, password = 'auth_user@test.ru', '1111'
        await client.post('auth/register', json=dict(
            email=email, password=password
        ))
        response = await client.post('auth/jwt/login', data=dict(
            username=email, password=password
        ))
        return {'booking_service': response.cookies['booking_service']}


@pytest.fixture(scope='session')
async def auth_user(get_cookie):
    async with AsyncClient(
            app=fast_api_app, base_url='http://test', cookies=get_cookie
    ) as client:
        yield client
