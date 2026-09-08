# 本模块方法
from .http_exception import BaseHttpException


class Http503ServiceUnavailableException(BaseHttpException):
    ServiceUnavailable = 503001  # 服务暂时不可用
    Maintenance = 503002  # 维护中

    def __init__(self, code, message, data=None):
        super().__init__(503, code, message, data)
