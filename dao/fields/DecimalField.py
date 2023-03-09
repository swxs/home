# -*- coding: utf-8 -*-
# @File    : DecimalField.py
# @AUTH    : swxs
# @Time    : 2019/4/2 13:49

# 本模块方法
from .BaseField import BaseField


class DecimalField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
