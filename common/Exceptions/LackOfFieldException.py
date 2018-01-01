# -*- coding: utf-8 -*-
import const


class LackOfFieldException(Exception):
    """
        缺少字段
    """

    def __init__(self, errmsg=None, data=None):
        self.code = const.AJAX_FAIL_NORMAL
        self.message = u"缺少{0}字段".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message
