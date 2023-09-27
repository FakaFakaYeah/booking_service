import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('email, password, status_code', [
    ('test@test.ru', '1234556', 201),
    ('test@test.ru', '1234556', 400),
    ('sdfsd', '1234556', 422),
])
async def test_register_user(
    test_client: AsyncClient,
    email, password, status_code
):

    response = await test_client.post(
        'auth/register', json=dict(email=email, password=password)
    )
    assert response.status_code == status_code
    print(response.status_code)
