from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import Users_crud


async def check_email(email, session: AsyncSession):

    results = await Users_crud.get_one(session=session, email=email)
    if results:
        raise HTTPException(
            status_code=400,
            detail=f'Пользователь с email: {email} уже зарегистрирован!'
        )