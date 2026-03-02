# 本模块方法
from .http_exception import BaseHttpException


class Http409ConflictException(BaseHttpException):
    ResourceConflict = 409001  # 资源冲突
    DuplicateSubmit = 409002  # 重复提交

    def __init__(self, code, message, data=None):
        super().__init__(409, code, message, data)
