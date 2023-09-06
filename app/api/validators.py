from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import Users_crud
from app.services import Password


async def check_email(email, session: AsyncSession):

    results = await Users_crud.get_one(session=session, email=email)
    if results:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Пользователь с email: {email} уже зарегистрирован!'
        )


async def check_login(email, password, session: AsyncSession):

    user = await Users_crud.get_one(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Пользователь с email: {email} не зарегистрирован!'
        )
    if not Password.verify_password(
            plain_password=password, hashed_password=user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Вы ввели неверные учетные данные'
        )
    return user
