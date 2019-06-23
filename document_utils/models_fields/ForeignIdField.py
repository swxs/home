# -*- coding: utf-8 -*-
# @File    : ForeignIdField.py
# @AUTH    : swxs
# @Time    : 2018/6/22 17:32

from . import BaseField
from . import ObjectIdField


class ForeignIdField(ObjectIdField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
