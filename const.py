# -*- coding: utf-8 -*-

import datetime
import hashlib
import requests

undefined = frozenset()

# undefined 最好是一个类，单例， 支持json， print等方法， 定义eq等方法
# class Undefined(object):
#     def __new__(cls):
#         pass
#
#     def __int__(self):
#         return frozenset()
#
#     def __str__(self):
#         pass

# undefined = Undefined()

AJAX_SUCCESS = 0
AJAX_FAIL_NORMAL = 1
AJAX_FAIL_AUTH = 2
AJAX_FAIL_NOTLOGIN = 3

ARTICAL_LIST_PER_PAGE = 20
USER_LIST_PER_PAGE = 20
TAG_LIST_PER_PAGE = 20
PASSWORDLOCK_LIST_PER_PAGE = 20

if __name__ == "__main__":
    pass
