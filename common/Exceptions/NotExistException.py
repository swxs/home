# -*- coding: utf-8 -*-
import const


class NotExistException(Exception):
    '''
        不存在
    '''

    def __init__(self, errmsg=None, data=None):
        self.code = const.AJAX_FAIL_NORMAL
        self.message = u"{0}不存在".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message
