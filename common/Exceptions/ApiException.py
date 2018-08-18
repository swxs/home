# -*- coding: utf-8 -*-
# @File    : ApiException.py
# @AUTH    : swxs
# @Time    : 2018/6/25 15:09

from api.consts.const import AJAX_FAIL_NORMAL


class ApiException(Exception):
    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_NORMAL
        self.message = errmsg or ""
        self.data = data

    def __str__(self):
        return self.message
