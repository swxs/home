# 本模块方法
from .http_exception import BaseHttpException


class Http500InternalServerErrorException(BaseHttpException):
    HelperServerError = 500001  # 第三方服务异常

    def __init__(self, code, message, data=None):
        super().__init__(500, code, message, data)
