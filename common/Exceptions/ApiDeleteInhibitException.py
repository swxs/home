# -*- coding: utf-8 -*-

from common.Exceptions.ApiException import ApiException


class ApiDeleteInhibitException(ApiException):
    def __init__(self, message=None, data=None):
        message_ = f"对象不可删除: {message}"
        super(ApiDeleteInhibitException, self).__init__(message=message_, data=data)
