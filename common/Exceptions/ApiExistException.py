# -*- coding: utf-8 -*-

from common.Exceptions.ApiException import ApiException


class ApiExistException(ApiException):
    def __init__(self, message, data=None):
        message_ = f"对象已存在: {message}"
        super(ApiExistException, self).__init__(message=message_, data=data)
