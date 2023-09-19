from datetime import date

from sqlalchemy import select, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Bookings, Rooms
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
        booking_rooms = await CRUDBase.get_all_bookings_with_user_date(
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

    @staticmethod
    async def get_all_user_bookings(
            user_id: int,
            session: AsyncSession
    ):
        user_bookings = select(
            Bookings.room_id,
            Bookings.user_id,
            Bookings.date_from,
            Bookings.date_to,
            Bookings.price,
            Bookings.total_cost,
            Bookings.total_days,
            Rooms.image_id,
            Rooms.name,
            Rooms.description,
            Rooms.services
        ).join(Rooms).where(Bookings.user_id == user_id)

        user_bookings = await session.execute(user_bookings)
        return user_bookings.all()


BookingsCrud = BookingCRUDBase(Bookings)
