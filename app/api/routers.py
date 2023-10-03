from fastapi import APIRouter

from app.api.endpoints import (
    bookings_router, users_router, hotels_router, rooms_router
)

main_router = APIRouter()
main_router.include_router(users_router)

main_router.include_router(
    bookings_router, prefix='/bookings', tags=['Бронирование']
)

main_router.include_router(
    hotels_router,
    prefix='/hotels',
    tags=['Отели']
)

main_router.include_router(
    rooms_router,
    prefix='/rooms',
    tags=['Номера']
)
