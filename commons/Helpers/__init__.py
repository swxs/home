import core

# 本模块方法
from . import Helper_JWT, Helper_encryption

encryption = Helper_encryption.Encryption(
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
