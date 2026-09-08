# 本模块方法
from .http_exception import BaseHttpException


class Http400BadRequestException(BaseHttpException):
    IllegalArgument = 400001  # 参数不合法
    NoResource = 400002  # 资源不存在
    DatabaseConstraintError = 400003  # 数据库约束错误（唯一约束、外键约束等）
    DatabaseDataError = 400004  # 数据库数据错误

    def __init__(self, code, message, data=None):
        super().__init__(400, code, message, data)
