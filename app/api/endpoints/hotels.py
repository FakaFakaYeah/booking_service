from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import HotelsCrud
from app.core import get_async_session
from app.schemas.hotels import HotelsLocationDB
from app.schemas.rooms import RoomsPriceDB


router = APIRouter()


@router.get(
    '/',
    summary='Получение списка отелей',
    response_model=list[HotelsLocationDB]
)
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
