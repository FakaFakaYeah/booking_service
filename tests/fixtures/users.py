import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import Users
from app.main import app as fast_api_app
from tests.constants import PASSWORD, AUTH_LOGIN


@pytest.fixture
async def test_client():
    async with AsyncClient(app=fast_api_app, base_url='http://test') as client:
        yield client


@pytest.fixture(scope='session')
async def get_cookie():

    async with AsyncClient(app=fast_api_app, base_url='http://test') as client:
        await client.post('auth/register', json=dict(
            email=AUTH_LOGIN, password=PASSWORD
        ))
        response = await client.post('auth/jwt/login', data=dict(
            username=AUTH_LOGIN, password=PASSWORD
        ))
        return {'booking_service': response.cookies['booking_service']}


@pytest.fixture(scope='session')
async def auth_user(get_cookie):
    async with AsyncClient(
            app=fast_api_app, base_url='http://test', cookies=get_cookie
    ) as client:
        yield client


@pytest.fixture
async def user_db_1(session: AsyncSession):

    user = Users(email='test_user1@test.ru', hashed_password=PASSWORD)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
