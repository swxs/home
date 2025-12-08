# -*- coding: utf-8 -*-
# @FILE    : utils/password_lock.py
# @AUTH    : model_creater

# 通用方法
from commons.Helpers import encryption

# 本模块方法
from . import consts


async def get_password(password_lock):
    if password_lock.ttype == consts.PasswordLock_Ttype.COMMON:
        if password_lock.key:
            password = encryption.get_password(name=password_lock.key)
        else:
            password = None
    elif password_lock.ttype == consts.PasswordLock_Ttype.CUSTOM:
        password = password_lock.custom.get("password", None)
    else:
        password = None

    return password
