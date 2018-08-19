# -*- coding: utf-8 -*-

from common.Exceptions.ApiException import ApiException


class ApiValidateException(ApiException):
    def __init__(self, errmsg, data=None):
        self.message = "{0}不合法".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message
