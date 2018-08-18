# -*- coding: utf-8 -*-
# @File    : BaseDocument.py
# @AUTH    : swxs
# @Time    : 2018/5/7 22:40

import datetime
from api.consts.const import undefined
import models_fields
from models_manager.manager_mongoenginee import Manager
from common.Decorator.Memorize import clear, upgrade, cache, memorize


class BaseMetaDocuemnt(type):
    def __new__(cls, name, bases, attrs):
        __fields__ = {}
        for attr_name, attr_value in attrs.items():
            if not isinstance(attr_value, models_fields.BaseField):
                continue
            attr_value.name = attr_name
            __fields__[attr_name] = attr_value
        attrs["__fields__"] = __fields__

        attrs["__model_name__"] = name
        return super(BaseMetaDocuemnt, cls).__new__(cls, name, bases, attrs)


class BaseDocument(object, metaclass=BaseMetaDocuemnt):
    __page_number__ = 20

    metaclass = BaseMetaDocuemnt

    def __init__(self, **kwargs):
        for attr in self.__fields__:
            self.__dict__[attr] = kwargs.get(attr, undefined)
        self.__dict__["id"] = kwargs.get("_id", undefined)

        self._data = {}
        for key, value in kwargs.items():
            self._data[key] = value

    @classmethod
    def get_instance(cls, model):
        data = dict()
        for attr in cls.__fields__:
            data[attr] = model.__getattribute__(attr)
        data["_id"] = str(model.__getattribute__("id"))
        return cls(**data)

    def to_dict(self):
        data = dict()
        data["id"] = self.__dict__["id"]
        for attr in self.__fields__:
            if self.__dict__[attr] != undefined:
                data[attr] = self.__dict__[attr]
        return data

    def to_front(self):
        data_dict = self.to_dict()
        for field_name, field_type in self.__fields__.items():
            if isinstance(field_type, models_fields.DateTimeField) and (field_name in data_dict):
                if isinstance(data_dict[field_name], datetime.datetime):
                    data_dict[field_name] = data_dict[field_name].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    data_dict[field_name] = None
        return data_dict

    @classmethod
    @upgrade
    def create(cls, **kwargs):
        return Manager.create(cls, **kwargs)

    @classmethod
    @cache
    def select(cls, **kwargs):
        return Manager.select(cls, **kwargs)

    @classmethod
    def filter(cls, *args, **kwargs):
        return Manager.filter(cls, *args, **kwargs)

    @upgrade
    def update(self, **kwargs):
        for key in self.__fields__:
            if self.__fields__[key].__getitem__("pre_update"):
                if callable(self.__fields__[key].pre_update):
                    kwargs[key] = self.__fields__[key].pre_update()
                else:
                    kwargs[key] = self.__fields__[key].pre_update
        return Manager.update(self, **kwargs)

    @clear
    def delete(self):
        return Manager.delete(self)
