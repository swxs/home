# -*- coding: utf-8 -*-

from api.consts.const import AJAX_FAIL_NOTLOGIN
from common.Exceptions.ApiException import ApiException

class ApiNotLoginException(ApiException):
    '''
        用户未登录
    '''
    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_NOTLOGIN
        self.message = errmsg or "用户未登录"
        self.data = data

    def __str__(self):
        return self.message
