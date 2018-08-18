# -*- coding: utf-8 -*-

from api.consts.const import AJAX_FAIL_NORMAL
from common.Exceptions.ApiException import ApiException

class ValidateException(ApiException):
    '''
        校验错误，字段错误
    '''

    def __init__(self, errmsg, data=None):
        self.code = AJAX_FAIL_NORMAL
        self.message = "{0}不合法".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message
