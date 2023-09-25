from passlib.context import CryptContext
from pydantic import EmailStr
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi import status

from app.core import settings
from app.core.db import async_session_maker
from app.crud import UsersCrud
from app.models import Users


async def get_user(email: EmailStr):
    async with async_session_maker() as session:
        user = await UsersCrud.get_one(session, email=email)
    return user


def verify_password(plain_password, hashed_password):

    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    return pwd_context.verify(plain_password, hashed_password)


class AdminAuth(AuthenticationBackend):
    async def login(
            self, request: Request,
    ) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user: Users = await get_user(email=email)
        if not user or not user.is_superuser:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        request.session.update({"token": '...'})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(
                request.url_for("admin:login"),
                status_code=status.HTTP_302_FOUND
            )
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
