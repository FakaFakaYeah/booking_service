from fastapi import APIRouter

from app.api.endpoints import bookings_router, users_router

main_router = APIRouter()
main_router.include_router(
    bookings_router, prefix='/bookings', tags=['Бронирование']
)
main_router.include_router(users_router)
