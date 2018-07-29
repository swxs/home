# -*- coding: utf-8 -*-
import const
from common.Exceptions.ApiException import ApiException

class ExistException(ApiException):
    '''
        字段已存在
    '''

    def __init__(self, errmsg, data=None):
        self.code = const.AJAX_FAIL_NORMAL
        self.message = "{0}已存在".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message
