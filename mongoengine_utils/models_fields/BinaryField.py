# -*- coding: utf-8 -*-
# @File    : BinaryField.py
# @AUTH    : swxs
# @Time    : 2019/4/2 14:08

from . import BaseField


class BinaryField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
