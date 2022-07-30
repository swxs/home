import core
from . import DBHelper_Redis
from . import Helper_JWT
from . import Helper_encryption


redis_helper = DBHelper_Redis.RedisDBHelper(
    db=core.config.REDIS_DB,
    host=core.config.REDIS_HOST,
    port=core.config.REDIS_PORT,
    password=core.config.REDIS_PASSWORD,
)

Encryption = Helper_encryption.Encryption(
    salt="b8862e668e5abbc99d8390347e7ac749",
)

tokener = Helper_JWT.Helper_JWT(
    key=core.config.JWT_SECRET_KEY,
    timeout=core.config.JWT_TIMEOUT,
)

refresh_tokener = Helper_JWT.Helper_JWT(
    key=core.config.JWT_SECRET_KEY,
    timeout=core.config.JWT_REFRESH_TIMEOUT,
)
