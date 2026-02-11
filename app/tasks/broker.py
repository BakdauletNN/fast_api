from celery import Celery
from app.config import stgs


celery_app = Celery(
    "tasks",
    broker=f"redis://{stgs.REDIS_HOST}:{stgs.REDIS_PORT}",
    include=["app.tasks.tasks"]
)