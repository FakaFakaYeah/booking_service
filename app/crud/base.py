from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:

    def __init__(self, model):
        self.__model = model

    async def get_all(self, session: AsyncSession):

        result = await session.scalars(select(self.__model))
        return result.all()
