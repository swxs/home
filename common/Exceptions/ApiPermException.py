# -*- coding: utf-8 -*-

from api.consts.const import AJAX_FAIL_AUTH
from common.Exceptions.ApiException import ApiException

class ApiPermException(ApiException):
    '''
        权限错误
    '''

    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_AUTH
        self.message = errmsg or "权限错误"
        self.data = None

    def __str__(self):
        return self.message
