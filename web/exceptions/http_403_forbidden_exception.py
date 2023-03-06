# 本模块方法
from .http_exception import BaseHttpException


class Http403ForbiddenException(BaseHttpException):
    PasswordError = 403001  # 用户名或密码不正确

    def __init__(self, code, message, data=None):
        super().__init__(403, code, message, data)
