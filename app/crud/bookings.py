from datetime import date

from sqlalchemy import select, and_, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Bookings, Rooms
from app.crud import CRUDBase
from app.services.exceptions import RoomCannotBeBooked


class BookingCRUDBase(CRUDBase):

    async def create(
            self,
            room_id: int,
            user_id: int,
            date_from: date,
            date_to: date,
            session: AsyncSession
    ):
        booking_rooms = CRUDBase.get_all_bookings_with_user_date(
            date_from=date_from, date_to=date_to
        )

        get_rooms_left = select(
            Rooms.quantity - func.count(booking_rooms.c.room_id)
        ).outerjoin(booking_rooms).where(Rooms.id == room_id).group_by(
            Rooms.id
        )

        rooms_left = await session.scalar(get_rooms_left)

        if rooms_left > 0:
            get_price = select(Rooms.price).filter_by(id=room_id)
            price = await session.scalar(get_price)
            add_booking = insert(Bookings).values(
                room_id=room_id, user_id=user_id, date_from=date_from,
                date_to=date_to, price=price
            )
            new_booking = await session.execute(add_booking)
            await session.commit()
            return new_booking.first()
        else:
            raise RoomCannotBeBooked


BookingsCrud = BookingCRUDBase(Bookings)
