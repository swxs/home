# -*- coding: utf-8 -*-

from api.consts.const import AJAX_FAIL_NORMAL
from common.Exceptions.ApiException import ApiException

class NotExistException(ApiException):
    '''
        不存在
    '''

    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_NORMAL
        self.message = "{0}不存在".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message
