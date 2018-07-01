# -*- coding: utf-8 -*-
# @File    : StringField.py
# @AUTH    : swxs
# @Time    : 2018/6/22 17:25

from common.Exceptions import ValidateException
from common.Utils.validate import Validate
from models_fields import BaseField


class StringField(BaseField):
    def __init__(self, validate=None, **kwargs):
        self.validate = validate
        super().__init__(**kwargs)

    def __set__(self, instance, value):
        if Validate.check(value, self.validate):
            raise ValidateException(self.name)
        super().__set__(instance, value)
