from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.users import auth_backend, fastapi_users, current_user
from app.schemas.users import UserCreate, UserRead
from app.core import get_async_session
from app.crud import UsersCrud
from app.models import Users

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)


@router.get(
    '/users/me',
    summary='Получить информацию о текущем пользователе',
    tags=['Пользователи'],
    response_model=UserRead
)
async def get_current_user(
    user: Users = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await UsersCrud.get_by_id(session=session, obj_id=user.id)
