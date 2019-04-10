# -*- coding: utf-8 -*-
# @File    : BaseDocument.py
# @AUTH    : swxs
# @Time    : 2018/5/7 22:40

import datetime

from bson import ObjectId
from tornado.util import ObjectDict
from api.BaseConsts import undefined
from common.Exceptions import *
from common.Utils.log_utils import getLogger
from .manager_mongoenginee import Manager
from .models_fields import *
from .Memorize import clear, upgrade, cache, memorize

log = getLogger("BaseDocument")


class BaseMetaDocuemnt(type):
    def __new__(cls, name, bases, attrs):
        __fields__ = {}
        parent = None
        for base in bases:
            if isinstance(base, cls) and (base.__model_name__ != 'BaseDocument'):
                parent = base
                for key, value in base.__fields__.items():
                    __fields__[key] = value

        for attr_name, attr_value in attrs.items():
            if not isinstance(attr_value, BaseField):
                continue
            attr_value.name = attr_name
            __fields__[attr_name] = attr_value
        attrs["__fields__"] = __fields__

        attrs["__subclass__"] = dict()
        attrs["__model_name__"] = name
        if 'meta' in attrs:
            meta_data: dict = attrs.get('meta', {})
            attrs["__base_model_name__"] = meta_data.get('inheritance', name)
        else:
            attrs["__base_model_name__"] = name

        current_class = super(BaseMetaDocuemnt, cls).__new__(cls, name, bases, attrs)
        if parent is not None:
            parent.__subclass__[name] = current_class
        return current_class


class BaseDocument(object, metaclass=BaseMetaDocuemnt):
    __page_number__ = 20

    metaclass = BaseMetaDocuemnt

    def __init__(self, **kwargs):
        self._raw_model = kwargs.get("_raw_model", undefined)

        for attr in self.__fields__:
            self.__dict__[attr] = kwargs.get(attr, undefined)
        self.__dict__["id"] = kwargs.get("_id", undefined)
        self.__dict__["oid"] = kwargs.get("_oid", undefined)

        self._data = {}
        for key, value in kwargs.items():
            self._data[key] = value

    @classmethod
    def get_instance(cls, model):
        data = dict()
        for attr in cls.__fields__:
            data[attr] = model.__getattribute__(attr)
        data["_oid"] = model.__getattribute__("id")
        data["_id"] = str(model.__getattribute__("id"))
        data["_raw_model"] = model
        return cls(**data)

    def update_instance(self, model):
        data = dict()
        for attr in self.__fields__:
            self.__setattr__(attr, model.__getattribute__(attr))
            self.__dict__[attr] = model.__getattribute__(attr)
        return self

    def to_dict(self, dict_factory=ObjectDict):
        data = dict_factory()
        data["id"] = self.__dict__["id"]
        for field_name, field_type in self.__fields__.items():
            if self.__getattribute__(field_name) != undefined:
                data[field_name] = self.__getattribute__(field_name)
        return data

    def to_front(self, dict_factory=ObjectDict):
        data_dict = self.to_dict(dict_factory=dict_factory)
        for field_name, field_type in self.__fields__.items():
            if isinstance(field_type, DateTimeField) and (field_name in data_dict):
                if isinstance(data_dict[field_name], datetime.datetime):
                    data_dict[field_name] = data_dict[field_name].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    data_dict[field_name] = None
        return data_dict

    @classmethod
    def is_exist(cls, *args, **kwargs):
        try:
            obj = Manager.select(cls, **kwargs)
            return True
        except ApiNotExistException:
            return False
        except Exception as e:
            log.error(e)
            return False

    @classmethod
    @upgrade
    def create(cls, **kwargs):
        log.info(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [create] <{cls.__model_name__}>: kwargs - {str(kwargs)}")
        return Manager.create(cls, **kwargs)

    @classmethod
    @cache
    def select(cls, **kwargs):
        log.info(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [select] <{cls.__model_name__}>: kwargs - {str(kwargs)}")
        return Manager.select(cls, **kwargs)

    @classmethod
    def filter(cls, *args, **kwargs):
        log.info(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [filter] <{cls.__model_name__}>: args - {str(args)} kwargs - {str(kwargs)}")
        return Manager.filter(cls, *args, **kwargs)

    @upgrade
    def update(self, **kwargs):
        for key in self.__fields__:
            if self.__fields__[key].__getattribute__("pre_update"):
                if callable(self.__fields__[key].pre_update):
                    kwargs[key] = self.__fields__[key].pre_update()
                else:
                    kwargs[key] = self.__fields__[key].pre_update
        log.info(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [update] <{self.__model_name__}>: kwargs - {str(kwargs)}")
        return Manager.update(self, **kwargs)

    @clear
    def delete(self):
        log.info(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [delete] <{self.__model_name__}>: kwargs - {str(dict(id=self.id))}")
        return Manager.delete(self)
