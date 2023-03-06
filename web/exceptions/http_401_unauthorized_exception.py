# 本模块方法
from .http_exception import BaseHttpException


class Http401UnauthorizedException(BaseHttpException):
    TokenLost = 401001
    TokenIllegal = 401002
    TokenTimeout = 401003

    def __init__(self, code, message, data=None):
        super().__init__(401, code, message, data)
