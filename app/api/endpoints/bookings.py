from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.crud import BookingsCrud
from app.schemas import BookingDB


router = APIRouter()


@router.get(
    '/',
    summary='Получить все букинги',
    response_model=list[BookingDB],
)
async def get_bookings(
        session: AsyncSession = Depends(get_async_session)
):
    return await BookingsCrud.get_all(session=session)

