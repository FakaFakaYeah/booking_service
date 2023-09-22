from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.api import main_router
from app.core import settings

app = FastAPI()
app.include_router(main_router)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url(
        settings.REDIS, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis=redis), prefix='booking-cache')


