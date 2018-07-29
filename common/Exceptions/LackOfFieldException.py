# -*- coding: utf-8 -*-
import const
from common.Exceptions.ApiException import ApiException

class LackOfFieldException(ApiException):
    """
        缺少字段
    """

    def __init__(self, errmsg=None, data=None):
        self.code = const.AJAX_FAIL_NORMAL
        self.message = "缺少{0}字段".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message
