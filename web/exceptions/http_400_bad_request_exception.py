# 本模块方法
from .http_exception import BaseHttpException


class Http400BadRequestException(BaseHttpException):
    IllegalArgument = 400001  # 参数不合法

    def __init__(self, code, message, data=None):
        super().__init__(400, code, message, data)
