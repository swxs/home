# 本模块方法
from .http_exception import BaseHttpException


class Http429TooManyRequestsException(BaseHttpException):
    RateLimitExceeded = 429001  # 请求过于频繁/限流

    def __init__(self, code, message, data=None):
        super().__init__(429, code, message, data)
