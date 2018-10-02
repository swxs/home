# -*- coding: utf-8 -*-

from enum import Enum

undefined = frozenset()


class HTTP_METHOD(Enum):
    GET = "GET"
    DELETE = "DELETE"


class HTTP_STATUS(Enum):
    AJAX_SUCCESS = 0
    AJAX_FAIL_NORMAL = 1  # 常规操作出错
    AJAX_FAIL_AUTH = 2  # 权限问题

    AJAX_FAIL_NOT_LOGIN = 3  # 用户未登录

    AJAX_FAIL_NOT_FOUND = 4  # 接口不存在
