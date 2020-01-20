# -*- coding: utf-8 -*-
# @File    : ApiException.py
# @AUTH    : swxs
# @Time    : 2018/6/25 15:09

from apps.BaseConsts import HTTP_STATUS


class ApiException(Exception):
    def __init__(self, code=HTTP_STATUS.AJAX_FAIL_NORMAL, message=None, data=None):
        self.code = code
        self.message = message or ""
        self.data = data
        self.status = 200

    def __str__(self):
        return self.message
