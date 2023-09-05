from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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

        result = await session.scalars(
            select(self.__model).filter_by(id=obj_id)
        )
        return result.first()

    async def create(self, obj_in, session: AsyncSession):

        obj = self.__model(**obj_in.dict())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj


