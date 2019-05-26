# -*- coding: utf-8 -*-
# @File    : Column.py
# @AUTH    : model_creater

from ..commons.Column import Column as BaseColumn


class Column(BaseColumn):
    def __init__(self, **kwargs):
        super(Column, self).__init__(**kwargs)
