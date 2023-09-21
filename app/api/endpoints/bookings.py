from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.crud import BookingsCrud, RoomsCrud
from app.schemas.bookings import BookingDB
from app.models import Users
from app.core.users import current_user
from app.api.validators import is_author_or_admin

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
    return await BookingsCrud.get_all_user_bookings(
        session=session, user_id=user.id
    )


@router.post(
    '/',
    summary='Бронирование номера',
)
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    session: AsyncSession = Depends(get_async_session),
    user: Users = Depends(current_user)
) -> dict[str, str]:
    """
    Бронирование номера пользователем
    - **room_id** - id номера, который нужно забронировать
    - **date_from** - с какого числа забронировать
    - **date_to** - по какое число забронировать
    """
    await RoomsCrud.get_by_id(session=session, obj_id=room_id)
    await BookingsCrud.create(
        room_id=room_id, user_id=user.id, date_from=date_from, date_to=date_to,
        session=session
    )
    return dict(detail='Номер успешно забронирован!')


@router.delete(
    '/{object_id}',
    summary='Удаление брони пользователя',
    description='Удаление доступно только админу или владельцу брони'
)
async def delete_booking(
        booking_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: Users = Depends(current_user)
) -> dict[str, str]:
    booking = await BookingsCrud.get_by_id(session=session, obj_id=booking_id)
    is_author_or_admin(obj=booking, user=user)
    await BookingsCrud.delete(session=session, obj=booking)
    return dict(detail='Бронь успешно удалена')
