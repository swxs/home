# -*- coding: utf-8 -*-
# @File    : BaseUtils.py
# @AUTH    : swxs
# @Time    : 2018/5/7 22:40

from const import undefined
from models_manager.manager_mongoenginee import Manager


class BaseUtils(object):
    __attrs__ = []

    def __init__(self, **kwargs):
        for attr in self.__attrs__:
            self.__dict__[attr] = kwargs.get(attr, undefined)
        self.__dict__["oid"] = kwargs.get("_id", undefined)

    @classmethod
    def get_instance(cls, model):
        data = dict()
        for attr in cls.__attrs__:
            data[attr] = model.__getattribute__(attr)
        data["_id"] = str(model.__getattribute__("id"))
        return cls(**data)

    def to_dict(self):
        data = dict()
        data["oid"] = self.__dict__["oid"]
        for attr in self.__attrs__:
            if self.__dict__[attr] != undefined:
                data[attr] = self.__dict__[attr]
        return data

    @classmethod
    def create(cls, **kwargs):
        return Manager.create(cls.__name__, cls, **kwargs)

    @classmethod
    def select(cls, **kwargs):
        return Manager.select(cls.__name__, cls, **kwargs)

    def udpate(self):
        return Manager.update(self.__name__, self)

    def delete(self):
        return Manager.delete(self.__name__, self)
