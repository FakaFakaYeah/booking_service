from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.schemas.rooms import RoomDB, RoomsCreate, RoomsUpdate
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


@router.patch(
    '/{room_id}',
    summary='Редактирование информации о номере',
    response_model=RoomDB,
    dependencies=[Depends(current_superuser)],
    description='Редактирование информации доступно только администратору'
)
async def room_update(
        room_id: int,
        room_upd: RoomsUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    room = await RoomsCrud.get_by_id(obj_id=room_id, session=session)
    if room_upd.hotel_id:
        await HotelsCrud.get_by_id(obj_id=room_upd.hotel_id, session=session)
    return await RoomsCrud.update(obj=room, obj_in=room_upd, session=session)


@router.delete(
    '/{room_id}',
    summary='Удаление номера',
    dependencies=[Depends(current_superuser)],
    description='Удалять номера может только администратор'
)
async def delete_room(
        room_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    room = await RoomsCrud.get_by_id(obj_id=room_id, session=session)
    await RoomsCrud.delete(obj=room, session=session)
