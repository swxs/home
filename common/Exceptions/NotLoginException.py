# -*- coding: utf-8 -*-
import const
from common.Exceptions.ApiException import ApiException

class NotLoginException(ApiException):
    '''
        用户未登录
    '''

    def __init__(self, errmsg=None, data=None):
        self.code = const.AJAX_FAIL_NOTLOGIN
        self.message = errmsg or "用户未登录"
        self.data = data

    def __str__(self):
        return self.message
