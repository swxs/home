# -*- coding: utf-8 -*-
# @File    : RegionException.py
# @AUTH    : swxs
# @Time    : 2018/9/20 13:59

class NotExistDealerInfoException(Exception):
    def __init__(self):
        pass


class NotExistDealerCodeInfoException(Exception):
    def __init__(self):
        pass


class MultiDealerInfoException(Exception):
    def __init__(self, multiple_list):
        self.multiple_list = multiple_list
