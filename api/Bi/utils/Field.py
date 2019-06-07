# -*- coding: utf-8 -*-
# @File    : Field.py
# @AUTH    : model_creater

from ..dao.Field import Field as BaseField


class Field(BaseField):
    def __init__(self, **kwargs):
        super(Field, self).__init__(**kwargs)
