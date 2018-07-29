# -*- coding: utf-8 -*-
import const
from common.Exceptions.ApiException import ApiException

class PermException(ApiException):
    '''
        权限错误
    '''

    def __init__(self, errmsg=None, data=None):
        self.code = const.AJAX_FAIL_AUTH
        self.message = errmsg or "权限错误"
        self.data = None

    def __str__(self):
        return self.message
