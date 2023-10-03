from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.schemas.rooms import RoomDB
from app.crud import RoomsCrud


router = APIRouter()


@router.get(
    '/{room_id}',
    summary='Получение информации по конкретному номеру',
    response_model=RoomDB
)
async def get_rooms(
        room_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await RoomsCrud.get_by_id(obj_id=room_id, session=session)
