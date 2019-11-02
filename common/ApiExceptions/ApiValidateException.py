# -*- coding: utf-8 -*-

from common.ApiExceptions.ApiException import ApiException


class ApiValidateException(ApiException):
    def __init__(self, message, data=None):
        message_ = f"参数不合法: {message}"
        super(ApiValidateException, self).__init__(message=message_, data=data)

