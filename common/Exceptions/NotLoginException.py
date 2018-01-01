# -*- coding: utf-8 -*-
import const


class NotLoginException(Exception):
    '''
        用户未登录
    '''

    def __init__(self, errmsg=None, data=None):
        self.code = const.AJAX_FAIL_NOTLOGIN
        self.message = errmsg or u"用户未登录"
        self.data = data

    def __str__(self):
        return self.message
