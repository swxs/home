# -*- coding: utf-8 -*-

from common.ApiExceptions.ApiException import ApiException


class ApiNotExistException(ApiException):
    def __init__(self, message=None, data=None):
        message_ = f"对象不存在: {message}"
        super(ApiNotExistException, self).__init__(message=message_, data=data)
