# -*- coding: utf-8 -*-

from enum import IntEnum

undefined = frozenset()

HTTP_METHOD_GET = "GET"
HTTP_METHOD_DELETE = "DELETE"


class HTTP_STATUS(IntEnum):
    AJAX_SUCCESS = 0
    AJAX_FAIL_NORMAL = 1  # 常规操作出错
    AJAX_FAIL_AUTH = 2  # 权限问题

    AJAX_FAIL_NOT_LOGIN = 3  # 用户未登录

    AJAX_FAIL_NOT_FOUND = 4  # 接口不存在

    AJAX_TOKEN_TIMEOUT = 5  # token已过期， 或者用户登出， token被加入黑名单

    AJAX_TOKEN_Illegal = 6  # token非法
