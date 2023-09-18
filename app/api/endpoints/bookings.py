from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.crud import BookingsCrud, RoomsCrud
from app.schemas.bookings import BookingDB
from app.models import Users
from app.core.users import current_user

router = APIRouter()


@router.get(
    '/',
    summary='Получить все бронирования текущего пользователя',
    response_model=list[BookingDB],
)
async def get_bookings(
        session: AsyncSession = Depends(get_async_session),
        user: Users = Depends(current_user)
):
    return await BookingsCrud.get_all(session=session, user_id=user.id)


@router.post(
    '/',
    summary='Бронирование номера'
)
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    session: AsyncSession = Depends(get_async_session),
    user: Users = Depends(current_user)
):
    await RoomsCrud.get_by_id(session=session, obj_id=room_id)
    await BookingsCrud.create(
        room_id=room_id, user_id=user.id, date_from=date_from, date_to=date_to,
        session=session
    )
    return dict(detail='Номер успешно забронирован!')
