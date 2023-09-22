from celery import Celery

from app.core import settings

celery = Celery(
    "tasks",
    broker=settings.REDIS,
    include=["app.tasks.tasks"]
)

