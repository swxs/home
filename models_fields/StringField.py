# -*- coding: utf-8 -*-
# @File    : StringField.py
# @AUTH    : swxs
# @Time    : 2018/6/22 17:25

from common.Exceptions import ApiValidateException
from common.Utils.validate import Validate
from models_fields import BaseField


class StringField(BaseField):
    def __init__(self, **kwargs):
        if "validate" in kwargs:
            self.validate = kwargs["validate"]
        super().__init__(**kwargs)

    def __set__(self, instance, value):
        if Validate.check(value, self.validate):
            raise ApiValidateException(self.name)
        super().__set__(instance, value)
