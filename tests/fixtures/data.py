import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Hotels, Rooms


@pytest.fixture(scope='session')
async def hotel_db(session: AsyncSession):

    hotel = Hotels(
        name='Test Hotel',
        location='Test location',
        services=[],
        rooms_quantity=10,
        image_id=1,
    )
    session.add(hotel)
    await session.commit()
    await session.refresh(hotel)
    return hotel


@pytest.fixture(scope='session')
async def room_db(session: AsyncSession, hotel_db):

    room = Rooms(
        hotel_id=hotel_db.id,
        name='Test room',
        description='Test',
        price=1000,
        services=[],
        quantity=10,
        image_id=1,
    )
    session.add(room)
    await session.commit()
    await session.refresh(room)
    return room
