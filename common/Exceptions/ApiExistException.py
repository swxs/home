# -*- coding: utf-8 -*-

from common.Exceptions.ApiException import ApiException


class ApiExistException(ApiException):
    def __init__(self, errmsg, data=None):
        self.message = "{0}已存在".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message
