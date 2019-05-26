# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model_creater

from ..dao.PasswordLock import PasswordLock as BasePasswordLock
from common.Helpers.Helper_encryption import Encryption


class PasswordLock(BasePasswordLock):
    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)

    @property
    def password(self):
        if self.key:
            return Encryption.get_password(name=self.key, salt="b8862e668e5abbc99d8390347e7ac749")
        else:
            return None

    def to_front(self, *args, **kwargs):
        data_dict = super(PasswordLock, self).to_front()
        data_dict["password"] = self.password
        return data_dict
