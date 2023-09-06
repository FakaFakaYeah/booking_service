from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UsersAuth, UsersDB
from app.core import get_async_session
from app.services import Password
from app.crud import Users_crud
from app.api.validators import check_email, check_login

router = APIRouter()


@router.post(
    '/register',
    summary='Регистрация пользователя',
    response_model=UsersDB
)
async def register_user(
    user: UsersAuth,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Регистрация пользователя

    - **email**: актуальный email
    - **password**: пароль от 6 до 16 символов без пробелов
    """
    await check_email(email=user.email, session=session)
    user.hashed_password = Password.get_password_hash(user.hashed_password)
    return await Users_crud.create(obj_in=user, session=session)


@router.post(
    '/login',
    summary='Аутентификация',
)
async def login_user(
    user_data: UsersAuth,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
):

    password = user_data.hashed_password
    user = await check_login(
        email=user_data.email, password=password, session=session
    )
    access_token = Password.create_access_token(sub=user.id)
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


