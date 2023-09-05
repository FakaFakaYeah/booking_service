from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import CreateUsers, UsersDB
from app.core import get_async_session
from app.services import Password
from app.crud import Users_crud
from app.api.validators import check_email

router = APIRouter()


@router.post(
    '/register',
    summary='Регистрация пользователя',
    response_model=UsersDB
)
async def register_user(
    user: CreateUsers,
    session: AsyncSession = Depends(get_async_session),
):
    await check_email(email=user.email, session=session)
    user.hashed_password = Password.get_password_hash(user.hashed_password)
    return await Users_crud.create(obj_in=user, session=session)



