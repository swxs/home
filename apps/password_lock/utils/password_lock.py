# -*- coding: utf-8 -*-
# @FILE    : utils/password_lock.py
# @AUTH    : model_creater

# 通用方法
from commons.Helpers.Helper_encryption import Encryption

# 本模块方法
from .. import consts
from ..dao.password_lock import PasswordLock


def password(self):
    if self.ttype == consts.PASSWORD_LOCK_TTYPE_COMMON:
        if self.key:
            return Encryption.get_password(name=self.key, salt=self.salt)
        else:
            return None
    elif self.ttype == consts.PASSWORD_LOCK_TTYPE_CUSTOM:
        return self.custom.get('password', None)
    else:
        return None


@PasswordLock.reload
async def to_front(self, *args, **kwargs):
    data_dict = await PasswordLock.to_front()
    data_dict["password"] = self.password
    return data_dict


@PasswordLock.add_search("website")
async def search_with_website(PasswordLock, **kwargs):
    return PasswordLock.filter(website__contains=kwargs.get("website"))


@PasswordLock.add_search("name")
async def search_with_name(PasswordLock, **kwargs):
    return PasswordLock.filter(name__contains=kwargs.get("name"))
