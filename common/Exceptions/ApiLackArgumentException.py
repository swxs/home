# -*- coding: utf-8 -*-

from api.consts.const import AJAX_FAIL_ILLEGAL
from common.Exceptions.ApiException import ApiException

class ApiLackArgumentException(ApiException):
    """
        缺少必要参数
    """
    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_ILLEGAL
        self.message = "参数不合法"
        self.data = data

    def __str__(self):
        return self.message
