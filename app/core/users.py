import re
from typing import Union

from fastapi import Depends
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, CookieTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.users import Users
from app.schemas.users import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, Users)


cookie_transport = CookieTransport(
    cookie_max_age=3600, cookie_name='booking_service', cookie_httponly=True
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[Users, int]):
    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, Users],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Пароль должен состоять минимум из 3 символов'
            )
        if len(password) > 16:
            raise InvalidPasswordException(
                reason='Пароль не должен превышать 16 символов'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль и email должны различаться'
            )
        if not re.search(r'^[a-zA-Zа-яА-Я0-9]+$', password):
            raise InvalidPasswordException(
                reason='Пароль должен состоять из букв и цифр без пробелов!'
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[Users, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
