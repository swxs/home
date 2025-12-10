# 本模块方法
from .http_exception import BaseHttpException


class Http500InternalServerErrorException(BaseHttpException):
    HelperServerError = 500001  # 第三方服务异常
    DatabaseError = 500002  # 数据库操作错误
    DatabaseConnectionError = 500003  # 数据库连接错误
    DatabaseProgrammingError = 500004  # 数据库编程错误（SQL语法错误等）

    def __init__(self, code, message, data=None):
        super().__init__(500, code, message, data)
