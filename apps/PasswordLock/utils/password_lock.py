# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model_creater

from marshmallow import Schema, fields
from .. import consts
from ..dao import PasswordLock as BasePasswordLock
from ..models import PasswordLock as PasswordLockModel
from commons.Helpers.Helper_encryption import Encryption

PasswordLockSchema = PasswordLockModel.schema.as_marshmallow_schema()

password_lock_schema = PasswordLockSchema()


class PasswordLock(BasePasswordLock):
    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)

    @property
    def password(self):
        if self.ttype == consts.PASSWORD_LOCK_TTYPE_COMMON:
            if self.key:
                return Encryption.get_password(name=self.key, salt="b8862e668e5abbc99d8390347e7ac749")
            else:
                return None
        elif self.ttype == consts.PASSWORD_LOCK_TTYPE_CUSTOM:
            return self.custom.get('password', None)
        else:
            return None

    async def to_front(self, *args, **kwargs):
        data_dict = await super(PasswordLock, self).to_front()
        data_dict["password"] = self.password
        return data_dict


@PasswordLock.add_search("website")
async def search_with_website(PasswordLock, **kwargs):
    return PasswordLock.filter(website__contains=kwargs.get("website"))


@PasswordLock.add_search("name")
async def search_with_name(PasswordLock, **kwargs):
    return PasswordLock.filter(name__contains=kwargs.get("name"))
