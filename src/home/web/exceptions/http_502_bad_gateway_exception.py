# 本模块方法
from .http_exception import BaseHttpException


class Http502BadGatewayException(BaseHttpException):
    UpstreamError = 502001  # 上游服务异常

    def __init__(self, code, message, data=None):
        super().__init__(502, code, message, data)
