# -*- coding: utf-8 -*-
# @File    : ForeignIdField.py
# @AUTH    : swxs
# @Time    : 2018/6/22 17:32

from models_fields import StringField


class ForeignIdField(StringField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
