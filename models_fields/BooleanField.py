# -*- coding: utf-8 -*-
# @File    : DateTimeField.py
# @AUTH    : swxs
# @Time    : 2018/6/22 17:35

from models_fields import BaseField


class BooleanField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
