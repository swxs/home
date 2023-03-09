# -*- coding: utf-8 -*-
# @File    : BaseField.py
# @AUTH    : swxs
# @Time    : 2018/6/22 17:26


class BaseField(object):
    name = None

    def __init__(self, **kwargs):
        self._virtual = kwargs.get("virtual", 0)
        self._convert = kwargs.get("convert", None)
        self._default_create = kwargs.get("default_create", None)
        self._default_update = kwargs.get("default_update", None)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._data.get(self.name)

    def __set__(self, instance, value):
        instance._data[self.name] = value

    @property
    def create_default(self):
        if callable(self._default_create):
            return self._default_create()
        else:
            return self._default_create

    @property
    def update_default(self):
        if callable(self._default_update):
            return self._default_update()
        else:
            return self._default_update

    @property
    def converts(self):
        return self._convert

    def to_dict(self, value):
        return str(value)
