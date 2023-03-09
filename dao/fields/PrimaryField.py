# -*- coding: utf-8 -*-
# @File    : ObjectIdField.py
# @AUTH    : swxs
# @Time    : 2019/4/2 11:14

# 本模块方法
from .BaseField import BaseField


class PrimaryField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
