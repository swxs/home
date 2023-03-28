# -*- coding: utf-8 -*-
# @FILE    : utils/password_lock.py
# @AUTH    : model_creater

# 通用方法
from commons.Helpers import encryption

# 本模块方法
from . import model_consts


async def to_front(password_lock):
    data = password_lock.to_dict()

    if password_lock.ttype == model_consts.PASSWORD_LOCK_TTYPE_COMMON:
        if password_lock.key:
            data["password"] = encryption.get_password(name=password_lock.key)
        else:
            data["password"] = None
    elif password_lock.ttype == model_consts.PASSWORD_LOCK_TTYPE_CUSTOM:
        data["password"] = password_lock.custom.get('password', None)
    else:
        data["password"] = None
    return data
