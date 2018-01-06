# -*- coding: utf-8 -*-
import const


class CommonException(Exception):
    '''
        非常规错误, 自定义返回内容
    '''

    def __init__(self, errmsg=None, data=None):
        self.code = const.AJAX_FAIL_NORMAL
        self.message = errmsg or ""
        self.data = data

    def __str__(self):
        return self.message