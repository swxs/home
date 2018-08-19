# -*- coding: utf-8 -*-

from common.Exceptions.ApiException import ApiException


class ApiDeleteInhibitException(ApiException):
    def __init__(self, errmsg=None, data=None):
        self.message = "{0}不可删除".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message
