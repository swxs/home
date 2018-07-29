# -*- coding: utf-8 -*-
# @File    : ListField.py
# @AUTH    : swxs
# @Time    : 2018/7/29 20:45

from models_fields import BaseField


class ListField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
