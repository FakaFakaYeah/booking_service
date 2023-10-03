from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.schemas.rooms import RoomDB, RoomsCreate
from app.crud import RoomsCrud, HotelsCrud
from app.core.users import current_superuser


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


@router.post(
    '/',
    summary='Добавление нового номера',
    response_model=RoomDB,
    dependencies=[Depends(current_superuser)],
    description='Добавление новой комнаты доступно только админу'
)
async def room_create(
        room: RoomsCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await HotelsCrud.get_by_id(obj_id=room.hotel_id, session=session)
    return await RoomsCrud.create(obj_in=room, session=session)
