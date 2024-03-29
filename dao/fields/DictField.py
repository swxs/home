# -*- coding: utf-8 -*-
# @File    : DictField.py
# @AUTH    : swxs
# @Time    : 2018/7/29 20:46

# 本模块方法
from .BaseField import BaseField


class DictField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self, value):
        return dict(value)
