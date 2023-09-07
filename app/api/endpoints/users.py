from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.users import auth_backend, fastapi_users, current_user
from app.schemas import UserCreate, UserRead, UserUpdate
from app.core import get_async_session
from app.crud import Users_crud
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
    tags=['Пользователи'],
    response_model=UserRead
)
async def get_current_user(
    user: Users = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await Users_crud.get_by_id(session=session, obj_id=user.id)