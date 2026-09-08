# 本模块方法
from .http_exception import BaseHttpException


class Http405MethodNotAllowedException(BaseHttpException):
    MethodNotAllowed = 405001  # 请求方法不允许

    def __init__(self, code, message, data=None):
        super().__init__(405, code, message, data)
