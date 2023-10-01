from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from app.core.users import current_superuser
from app.crud import HotelsCrud
from app.core import get_async_session
from app.schemas.hotels import (
    HotelsDB, HotelsRoomsLeft, HotelCreate, HotelUpdate
)
from app.schemas.rooms import RoomsPriceDB


router = APIRouter()


@router.get(
    '/{hotel_id}',
    summary='Получаем информацию по конкретному отелю',
    response_model=HotelsDB
)
async def get_hotel(
        hotel_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await HotelsCrud.get_by_id(obj_id=hotel_id, session=session)


@router.post(
    '/',
    summary='Добавление нового Отеля',
    dependencies=[Depends(current_superuser)],
    response_model=HotelsDB,
    description='Добавление нового отеля доступно только администратору'
)
async def create_hotel(
    hotel: HotelCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await HotelsCrud.create(obj_in=hotel, session=session)


@router.patch(
    '/hotel_id',
    summary='Обновление информации об отеле',
    response_model=HotelsDB,
    dependencies=[Depends(current_superuser)],
    description='Обновление информации об отели доступно только администратору'
)
async def update_hotel(
        hotel_id: int,
        hotel_update: HotelUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    hotel = await HotelsCrud.get_by_id(obj_id=hotel_id, session=session)
    return await HotelsCrud.update(
        obj=hotel, obj_in=hotel_update, session=session
    )


@router.get(
    '/',
    summary='Получение списка отелей',
    response_model=list[HotelsRoomsLeft]
)
@cache(expire=30)
async def get_all_hotels(
    date_from: date,
    date_to: date,
    location: str = Query(''),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получаем список отелей со свободными номерами за указанную период.
    - Опционально можно указать **location**, тогда поиск будет вестись
    по конкретному location
    """

    hotels = await HotelsCrud.get_all_with_location(
        location=location, date_from=date_from, date_to=date_to,
        session=session
    )
    return hotels


@router.get(
    '/{hotel_id}/rooms/',
    summary='Получение всех номеров отеля',
    response_model=list[RoomsPriceDB]
)
async def get_hotel_rooms(
        hotel_id: int,
        date_from: date,
        date_to: date,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Получаем список номеров конкретного отеля за указанный период.
    Дополнительно выводится кол-во свободных номеров каждого типа
    """
    await HotelsCrud.get_by_id(obj_id=hotel_id, session=session)
    rooms = await HotelsCrud.get_all_hotel_rooms(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to,
        session=session
    )
    return rooms
