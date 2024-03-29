# -*- coding: utf-8 -*-
# @FILE    : consts.py
# @AUTH    : model_creater


from enum import Enum

USER_AUTH_TTYPE_SUPERADMIN = 1
USER_AUTH_TTYPE_PASSWORD = 2
USER_AUTH_TTYPE_WECHAT = 3
USER_AUTH_TTYPE_PHONE = 4
USER_AUTH_TTYPE_EMAIL = 5

USER_AUTH_TTYPE_LIST = [
    (USER_AUTH_TTYPE_SUPERADMIN, '超管'),
    (USER_AUTH_TTYPE_PASSWORD, '账号密码'),
    (USER_AUTH_TTYPE_WECHAT, '微信'),
    (USER_AUTH_TTYPE_PHONE, '手机号'),
    (USER_AUTH_TTYPE_EMAIL, '邮箱'),
]

USER_AUTH_IFVERIFIED_TRUE = 1
USER_AUTH_IFVERIFIED_FALSE = 2

USER_AUTH_IFVERIFIED_LIST = [
    (USER_AUTH_IFVERIFIED_TRUE, '是'),
    (USER_AUTH_IFVERIFIED_FALSE, '否'),
]
