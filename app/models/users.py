from sqlalchemy.orm import relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core import Base


class Users(Base, SQLAlchemyBaseUserTable[int]):

    bookings = relationship("Bookings", back_populates='user')

    def __repr__(self):
        return f'Пользователь {self.email}'
