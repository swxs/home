# -*- coding: utf-8 -*-
# @File    : StringField.py
# @AUTH    : swxs
# @Time    : 2018/6/22 17:25

from . import BaseField


class StringField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
