from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.crud import BookingsCrud
from app.schemas.bookings import BookingDB
from app.models import Users
from app.core.users import current_user
from app.services.exceptions import RoomCannotBeBooked

router = APIRouter()


@router.get(
    '/',
    summary='Получить все букинги текущего пользователя',
    response_model=list[BookingDB],
)
async def get_bookings(
        session: AsyncSession = Depends(get_async_session),
        user: Users = Depends(current_user)
):
    return await BookingsCrud.get_all(session=session, user_id=user.id)


@router.post('/')
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    session: AsyncSession = Depends(get_async_session),
    user: Users = Depends(current_user)
):
    booking = await BookingsCrud.create(
        room_id=room_id, user_id=user.id, date_from=date_from, date_to=date_to,
        session=session
    )
    if not booking:
        raise RoomCannotBeBooked
    return dict(detail='Номер успешно забронирован!')
