import settings
from . import DBHelper_Redis


redis_helper = DBHelper_Redis.RedisDBHelper(
    db=settings.REDIS_DB, host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD
)
