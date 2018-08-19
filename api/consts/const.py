# -*- coding: utf-8 -*-

undefined = frozenset()

HTTP_METHOD_GET = "GET"

AJAX_SUCCESS = 0
AJAX_FAIL_NORMAL = 1  # 常规操作出错
AJAX_FAIL_AUTH = 2  # 权限问题
AJAX_FAIL_NOTLOGIN = 3  # 用户未登录
AJAX_FAIL_ILLEGAL = 4  # 参数不合法， 缺失或校验未通过
