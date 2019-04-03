# -*- coding: utf-8 -*-
# @File    : BaseField.py
# @AUTH    : swxs
# @Time    : 2018/6/22 17:26

class BaseField(object):
    name = None

    def __init__(self, **kwargs):
        self.pre_update = kwargs.get("pre_update", None)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._data.get(self.name)

    def __set__(self, instance, value):
        instance._data[self.name] = value
