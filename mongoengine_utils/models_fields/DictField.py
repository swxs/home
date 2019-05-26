# -*- coding: utf-8 -*-
# @File    : DictField.py
# @AUTH    : swxs
# @Time    : 2018/7/29 20:46

from . import BaseField


class DictField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
