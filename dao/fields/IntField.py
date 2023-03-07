# -*- coding: utf-8 -*-
# @File    : IntField.py
# @AUTH    : swxs
# @Time    : 2018/7/29 21:03

# 本模块方法
from . import BaseField


class IntField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self, value):
        return int(value)
