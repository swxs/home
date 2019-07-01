# -*- coding: utf-8 -*-
# @File    : FloatField.py
# @AUTH    : swxs
# @Time    : 2019/4/2 11:19

from . import BaseField


class FloatField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
