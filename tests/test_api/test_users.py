from httpx import AsyncClient

from tests.constants import PASSWORD

async def test_register_user(test_client: AsyncClient):

    response = await test_client.post(
        'auth/register', json=dict(email='test@test.ru', password=PASSWORD)
    )
    assert response.status_code == 201


async def test_register_user_email_exists(test_client: AsyncClient):
    response = await test_client.post(
        'auth/register', json=dict(email='test@test.ru', password=PASSWORD)
    )
    assert response.status_code == 400


async def test_logout_user(auth_user: AsyncClient):

    response = await auth_user.post('auth/jwt/logout')
    print(response.status_code)
