import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import Users


@pytest.fixture
async def user_db_1(session: AsyncSession):

    user = Users(email='test1@test.ru', hashed_password='12312312')
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
