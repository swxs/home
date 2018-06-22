# -*- coding: utf-8 -*-
# @File    : PasswordField.py
# @AUTH    : swxs
# @Time    : 2018/5/8 14:28

from common.Utils.validate import Validate, RegType
from models_fields import StringField

def get_password(value):
    pass

class PasswordField(StringField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
