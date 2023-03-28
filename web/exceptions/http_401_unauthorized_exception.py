# 本模块方法
from .http_exception import BaseHttpException


class Http401UnauthorizedException(BaseHttpException):
    TokenLost = 401001  # token不存在
    TokenIllegal = 401002  # token非法
    TokenTimeout = 401003  # token超时

    def __init__(self, code, message, data=None):
        super().__init__(401, code, message, data)
