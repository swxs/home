# -*- coding: utf-8 -*-
# @FILE    : consts.py
# @AUTH    : model_creater


from enum import IntEnum


class UserAuth_Ttype(IntEnum):
    PASSWORD = 1
    WECHAT = 2
    PHONE = 3
    EMAIL = 4


class UserAuth_Ifverified(IntEnum):
    VERIFIED = 1
    UNVERIFIED = 2


class OAuthClient_IsActive(IntEnum):
    ACTIVE = 1
    INACTIVE = 2
