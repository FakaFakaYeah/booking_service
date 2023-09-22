from datetime import date

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models import Hotels, Rooms


class HotelsCrudBase(CRUDBase):

    @staticmethod
    async def get_all_with_location(
            location: str,
            date_from: date,
            date_to: date,
            session: AsyncSession
    ):
        booking_rooms = await CRUDBase.get_all_bookings_with_user_date(
            date_from=date_from, date_to=date_to
        )

        rooms_hotels = select(
            Rooms.hotel_id, func.count(booking_rooms.c.id)
        ).outerjoin(booking_rooms).group_by(Rooms.hotel_id).cte('rooms_hotels')

        hotels = select(
            Hotels.id,Hotels.name,
            Hotels.location,
            Hotels.services,
            Hotels.rooms_quantity,
            Hotels.image_id,
            (Hotels.rooms_quantity - rooms_hotels.c.count).label('rooms_left')
        ).join(rooms_hotels).where(
            and_(
                Hotels.location.like(f'%{location}%'),
                Hotels.rooms_quantity - rooms_hotels.c.count > 0
            )
        ).order_by(Hotels.id)
        hotels = await session.execute(hotels)
        return hotels.mappings()

    @staticmethod
    async def get_all_hotel_rooms(
            hotel_id: int,
            date_from: date,
            date_to: date,
            session: AsyncSession
    ):
        booking_rooms = await CRUDBase.get_all_bookings_with_user_date(
            date_from=date_from, date_to=date_to
        )

        rooms = select(
            Rooms.id,
            Rooms.hotel_id,
            Rooms.name,
            Rooms.description,
            Rooms.services,
            Rooms.price,
            Rooms.quantity,
            Rooms.image_id,
            (Rooms.quantity - func.count(booking_rooms.c.room_id)).label(
                'rooms_left'
            ),
            (Rooms.price * (date_to - date_from).days).label('total_coast')
        ).outerjoin(booking_rooms).where(Rooms.hotel_id == hotel_id).group_by(
            Rooms.id
        )

        rooms = await session.execute(rooms)
        return rooms.all()


HotelsCrud = HotelsCrudBase(Hotels)
