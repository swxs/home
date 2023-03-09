# -*- coding: utf-8 -*-
# @File    : ForeignIdField.py
# @AUTH    : swxs
# @Time    : 2018/6/22 17:32

# 本模块方法
from .BaseField import BaseField
from .ObjectIdField import ObjectIdField


class ForeignIdField(ObjectIdField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
