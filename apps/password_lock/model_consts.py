# -*- coding: utf-8 -*-
# @FILE    : model_consts.py
# @AUTH    : model_creater


from enum import Enum

PASSWORD_LOCK_TTYPE_COMMON = 1
PASSWORD_LOCK_TTYPE_CUSTOM = 2

PASSWORD_LOCK_TTYPE_LIST = [
    (PASSWORD_LOCK_TTYPE_COMMON, '普通'),
    (PASSWORD_LOCK_TTYPE_CUSTOM, '自定义'),
]
