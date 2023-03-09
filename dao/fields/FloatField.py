# -*- coding: utf-8 -*-
# @File    : FloatField.py
# @AUTH    : swxs
# @Time    : 2019/4/2 11:19

# 本模块方法
from .BaseField import BaseField


class FloatField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self, value):
        return float(value)
