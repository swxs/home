# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model_creater

from ..commons.PasswordLock import PasswordLock as BasePasswordLock


class PasswordLock(BasePasswordLock):
    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)
