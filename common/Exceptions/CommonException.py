# -*- coding: utf-8 -*-
from api.consts.const import AJAX_FAIL_NORMAL
from common.Exceptions.ApiException import ApiException

class CommonException(ApiException):
    '''
        非常规错误, 自定义返回内容
    '''

    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_NORMAL
        self.message = errmsg or ""
        self.data = data

    def __str__(self):
        return self.message
