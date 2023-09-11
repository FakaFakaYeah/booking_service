from datetime import date

from sqlalchemy import select, and_, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Bookings, Rooms
from app.crud import CRUDBase


class BookingCRUDBase(CRUDBase):

    async def create(
            self,
            room_id: int,
            user_id: int,
            date_from: date,
            date_to: date,
            session: AsyncSession
    ):
        booked_rooms = select(Bookings).where(
            and_(
                Bookings.room_id == room_id,
                and_(
                    Bookings.date_from < date_to, Bookings.date_to > date_from
                )
            )
        ).cte("booked_rooms")

        get_rooms_left = select(
            Rooms.quantity - func.count(booked_rooms.c.room_id)
        ).join(
            booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
        ).where(Rooms.id == room_id).group_by(Rooms.id)

        rooms_left = await session.scalars(get_rooms_left)
        rooms_left = rooms_left.first()

        if rooms_left > 0:
            get_price = select(Rooms.price).filter_by(id=room_id)
            price = await session.scalars(get_price)
            price = price.first()
            add_booking = insert(Bookings).values(
                room_id=room_id, user_id=user_id, date_from=date_from,
                date_to=date_to, price=price
            ).returning(Bookings)
            new_booking = await session.scalars(add_booking)
            await session.commit()
            return new_booking.first()
        else:
            return None


BookingsCrud = BookingCRUDBase(Bookings)
