from datetime import date

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import ObjNotFound
from app.models import Bookings


class CRUDBase:

    def __init__(self, model):
        self.__model = model

    async def get_all(self, session: AsyncSession, **param):

        result = await session.scalars(select(self.__model).filter_by(**param))
        return result.all()

    async def get_one(self, session: AsyncSession, **param):

        result = await session.scalars(select(self.__model).filter_by(**param))
        return result.first()

    async def get_by_id(self, obj_id: int, session: AsyncSession):

        result = await session.scalar(
            select(self.__model).filter_by(id=obj_id)
        )
        if not result:
            raise ObjNotFound
        return result

    async def create(self, obj_in, session: AsyncSession):

        obj = self.__model(**obj_in.dict())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @staticmethod
    async def delete(obj, session: AsyncSession) -> None:
        await session.delete(obj)
        await session.commit()

    @staticmethod
    async def get_all_bookings_with_user_date(
            date_from: date,
            date_to: date,
    ):
        return select(Bookings).where(
            and_(
                Bookings.date_from < date_to,
                Bookings.date_to > date_from
            )
        ).cte('booking_rooms')

