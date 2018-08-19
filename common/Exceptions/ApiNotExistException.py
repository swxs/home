# -*- coding: utf-8 -*-

from common.Exceptions.ApiException import ApiException


class ApiNotExistException(ApiException):
    def __init__(self, errmsg=None, data=None):
        self.message = "{0}不存在".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message
