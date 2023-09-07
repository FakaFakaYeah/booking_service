from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.crud import BookingsCrud
from app.schemas import BookingDB
from app.models import Users
from app.services.auth import get_current_user

router = APIRouter()


@router.get(
    '/',
    summary='Получить все букинги текущего пользователя',
    response_model=list[BookingDB],
)
async def get_bookings(
        session: AsyncSession = Depends(get_async_session),
        user: Users = Depends(get_current_user)
):
    return await BookingsCrud.get_all(session=session, user_id=user.id)

