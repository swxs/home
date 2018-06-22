# -*- coding: utf-8 -*-
# @File    : BaseField.py
# @AUTH    : swxs
# @Time    : 2018/6/22 17:26

class BaseField(object):
    name = None

    def __init__(self, **kwargs):
        pass

    def __get__(self, instance, owner):
        if instance is None:
            return self
        print(self.name)
        return instance._data.get(self.name)

    def __set__(self, instance, value):
        if value is None:
            value = None
        instance._data[self.name] = value
