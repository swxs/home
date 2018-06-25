# -*- coding: utf-8 -*-
# @File    : ApiException.py
# @AUTH    : swxs
# @Time    : 2018/6/25 15:09

import const

class ApiException(Exception):
    def __init__(self, errmsg=None, data=None):
        self.code = const.AJAX_FAIL_NORMAL
        self.message = errmsg or ""
        self.data = data

    def __str__(self):
        return self.message