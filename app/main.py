from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.api import main_router
from app.core import settings
from app.core.db import engine
from app.core.admin import UserAdmin, BookingAdmin, HotelAdmin, RoomAdmin

app = FastAPI()
app.include_router(main_router)

admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url(
        settings.REDIS, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis=redis), prefix='booking-cache')