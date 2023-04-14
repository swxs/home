# -*- coding: utf-8 -*-
# @FILE    : utils/password_lock.py
# @AUTH    : model_creater

# 通用方法
from commons.Helpers import encryption

# 本模块方法
from . import model_consts


async def get_password(password_lock):
    if password_lock.ttype == model_consts.PASSWORD_LOCK_TTYPE_COMMON:
        if password_lock.key:
            password = encryption.get_password(name=password_lock.key)
        else:
            password = None
    elif password_lock.ttype == model_consts.PASSWORD_LOCK_TTYPE_CUSTOM:
        password = password_lock.custom.get('password', None)
    else:
        password = None

    return password


async def to_front(password_lock):
    data = password_lock.to_dict()

    data["password"] = get_password(get_password)

    return data
