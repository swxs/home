# 本模块方法
from .http_exception import BaseHttpException


class Http404NotFoundException(BaseHttpException):
    MethodNotFoundError = 404001  # 路径不存在

    def __init__(self, code, message, data=None):
        super().__init__(404, code, message, data)
