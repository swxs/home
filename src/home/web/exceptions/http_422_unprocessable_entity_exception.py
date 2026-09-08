# 本模块方法
from .http_exception import BaseHttpException


class Http422UnprocessableEntityException(BaseHttpException):
    ValidationError = 422001  # 参数校验失败
    BusinessValidationError = 422002  # 业务校验失败

    def __init__(self, code, message, data=None):
        super().__init__(422, code, message, data)
