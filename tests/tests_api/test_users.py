from httpx import AsyncClient


async def test_register_user(test_client: AsyncClient):

    response = await test_client.post(
        'auth/register', json=dict(email='test@test.ru', password='2354656')
    )
    assert response.status_code == 201


async def test_register_user_email_exists(test_client: AsyncClient):
    response = await test_client.post(
        'auth/register', json=dict(email='test@test.ru', password='2354656')
    )
    assert response.status_code == 400
    