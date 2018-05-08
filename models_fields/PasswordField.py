# -*- coding: utf-8 -*-
# @File    : PasswordField.py
# @AUTH    : swxs
# @Time    : 2018/5/8 14:28

from mongoengine import StringField
from common.Utils import utils
from const import undefined


class PasswordField(StringField):
    def __set__(self, instance, value):
        if value is None:
            value = None
        else:
            value = utils.get_password(value)
        super(PasswordField, self).__set__(instance, value)
