from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.crud import BookingsCrud


router = APIRouter()


@router.get('/')
async def get_bookings(
        session: AsyncSession = Depends(get_async_session)
):
    return await BookingsCrud.get_all(session=session)

