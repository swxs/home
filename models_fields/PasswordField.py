# -*- coding: utf-8 -*-
# @File    : PasswordField.py
# @AUTH    : swxs
# @Time    : 2018/5/8 14:28

from mongoengine import StringField
from common.Utils import utils
from common.Utils.validate import Validate, RegType


class PasswordField(StringField):
    def __set__(self, instance, value):
        if value is None:
            value = None
        elif not Validate.check(value, RegType.CHANGED_PASSWORD):
            value = utils.get_password(value)
        super(PasswordField, self).__set__(instance, value)
