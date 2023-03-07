# -*- coding: utf-8 -*-
# @File    : BaseField.py
# @AUTH    : swxs
# @Time    : 2018/6/22 17:26


class BaseField(object):
    name = None

    def __init__(self, **kwargs):
        self.create = kwargs.get("create", True)
        self.default_create = kwargs.get("default_create", None)
        self.default_update = kwargs.get("default_update", None)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._data.get(self.name)

    def __set__(self, instance, value):
        instance._data[self.name] = value

    @property
    def create_default(self):
        if callable(self.default_create):
            return self.default_create()
        else:
            return self.default_create

    @property
    def update_default(self):
        if callable(self.default_update):
            return self.default_update()
        else:
            return self.default_update

    def to_dict(self, value):
        return str(value)
