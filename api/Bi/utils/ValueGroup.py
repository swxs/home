# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model_creater

from ..commons.ValueGroup import ValueGroup as BaseValueGroup


class ValueGroup(BaseValueGroup):
    def __init__(self, **kwargs):
        super(ValueGroup, self).__init__(**kwargs)
