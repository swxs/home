# -*- coding: utf-8 -*-
import const


class ValidateException(Exception):
    '''
        校验错误，字段错误
    '''

    def __init__(self, errmsg, data=None):
        self.code = const.AJAX_FAIL_NORMAL
        self.message = u"{0}不合法".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message
