# -*- coding: utf-8 -*-
# @File    : ObjectIdField.py
# @AUTH    : swxs
# @Time    : 2019/4/2 11:14

from . import BaseField


class ObjectIdField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
