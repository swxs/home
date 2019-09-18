# -*- coding: utf-8 -*-
# @File    : BaseDocument.py
# @AUTH    : swxs
# @Time    : 2018/5/7 22:40

import datetime
import functools
import hashlib
from functools import wraps
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
            if isinstance(base, cls) and (getattr(base, "__model_name__") != 'BaseDocument'):
                parent = base
                for key, value in base.__fields__.items():
                    __fields__[key] = value

        for attr_name, attr_value in attrs.items():
            if not isinstance(attr_value, BaseField):
                continue
            attr_value.name = attr_name
            __fields__[attr_name] = attr_value
        attrs["__fields__"] = __fields__

        attrs["__search__"] = dict()
        attrs["__subclass__"] = dict()
        attrs["__model_name__"] = name
        if 'meta' in attrs:
            meta_data: dict = attrs.get('meta', {})
            attrs["__base_model_name__"] = meta_data.get('inheritance', name)
        else:
            attrs["__base_model_name__"] = name

        current_class = super(BaseMetaDocuemnt, cls).__new__(cls, name, bases, attrs)
        if parent is not None:
            getattr(parent, "__subclass__")[name] = current_class
        return current_class


class BaseDocument(object, metaclass=BaseMetaDocuemnt):
    __page_number__ = 20

    metaclass = BaseMetaDocuemnt

    def __init__(self, **kwargs):
        self.__raw_model__ = kwargs.get("__raw_model__", undefined)

        for attr in self.__fields__:
            self.__dict__[attr] = kwargs.get(attr, undefined)
        self.id = kwargs.get("_id", undefined)
        self.oid = kwargs.get("_oid", undefined)

        self._data = {}
        for key, value in kwargs.items():
            self._data[key] = value

    @classmethod
    def schema(cls):
        return getattr(cls, "__raw_model__").schema.as_marshmallow_schema()()

    @classmethod
    def get_instance(cls, model, _filter=None):
        if _filter is None:
            _filter = dict()

        data = dict()
        if "only" in _filter:
            all_fields = _filter["only"]
        else:
            all_fields = cls.__fields__

        for attr in all_fields:
            if ("exclude" in _filter) and (attr in _filter["exclude"]):
                continue
            data[attr] = getattr(model, attr)
        data["_id"] = str(getattr(model, "id"))
        data["_oid"] = getattr(model, "id")
        data["__raw_model__"] = model
        return cls(**data)

    def to_dict(self, dict_factory=ObjectDict):
        data = dict_factory()
        data["id"] = self.__dict__["id"]
        for field_name, field_type in self.__fields__.items():
            if self.__getattribute__(field_name) != undefined:
                data[field_name] = self.__getattribute__(field_name)
        return data

    async def to_front(self, dict_factory=ObjectDict):
        data_dict = self.to_dict(dict_factory=dict_factory)
        for field_name, field_type in self.__fields__.items():
            if isinstance(field_type, DateTimeField) and (field_name in data_dict):
                if isinstance(data_dict[field_name], datetime.datetime):
                    data_dict[field_name] = data_dict[field_name].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    data_dict[field_name] = None
        return data_dict

    @classmethod
    def is_exist(cls, **kwargs):
        try:
            obj = Manager.select(cls, **kwargs)
            return True
        except ApiNotExistException:
            return False
        except Exception as e:
            log.error(e)
            return False

    @staticmethod
    def get_key_with_list(params):
        params.sort()
        return hashlib.md5(b"".join(p.encode("utf8") for p in params)).hexdigest()

    @staticmethod
    def get_key_with_params(**kwargs):
        params = list(kwargs.keys())
        return BaseDocument.get_key_with_list(params)

    @classmethod
    @upgrade
    async def create(cls, **kwargs):
        for key in cls.__fields__:
            if not getattr(cls.__fields__[key], "create"):
                if key in kwargs:
                    del kwargs[key]
        log.info(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [create] <{getattr(cls, '__model_name__')}>: kwargs - {str(kwargs)}")
        return await Manager.create(cls, **kwargs)

    @classmethod
    @cache
    async def select(cls, **kwargs):
        log.info(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [select] <{getattr(cls, '__model_name__')}>: kwargs - {str(kwargs)}")
        if "id" in kwargs:
            kwargs["_id"] = ObjectId(kwargs["id"])
            kwargs.pop("id")
        return await Manager.select(cls, **kwargs)

    @classmethod
    async def filter(cls, **kwargs):
        log.info(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [filter] <{getattr(cls, '__model_name__')}>: kwargs - {str(kwargs)}")
        return await Manager.filter(cls, **kwargs)

    @classmethod
    def search(cls, **kwargs):
        log.info(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [search] <{getattr(cls, '__model_name__')}>: kwargs - {str(kwargs)}")
        key = cls.get_key_with_params(**kwargs)
        if key in getattr(cls, '__search__'):
            return getattr(cls, '__search__')[key](cls, **kwargs)
        else:
            return Manager.filter(cls, **kwargs)

    @upgrade
    async def update(self, **kwargs):
        for key in self.__fields__:
            if self.__fields__[key].__getattribute__("pre_update"):
                if callable(self.__fields__[key].pre_update):
                    kwargs[key] = self.__fields__[key].pre_update()
                else:
                    kwargs[key] = self.__fields__[key].pre_update
        log.info(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [update] <{getattr(self, '__model_name__')}>: kwargs - {str(kwargs)}")
        return await Manager.update(self, **kwargs)

    async def copy(self, **kwargs):
        params = self.to_dict(dict_factory=dict)
        for attr in self.__fields__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                if isinstance(self.__fields__[attr], DictField):
                    params[attr].update(value)
                else:
                    params[attr] = value
        return await self.__class__.create(**params)

    @clear
    async def delete(self):
        log.info(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [delete] <{getattr(self, '__model_name__')}>: kwargs - {str(dict(id=self.id))}")
        return await Manager.delete(self)

    @classmethod
    def add_search(cls, *args):
        key = cls.get_key_with_list(list(args))
        if key not in getattr(cls, "__search__"):
            def wrapper(function):
                @wraps(function)
                def inner_wrapper(*args, **kwargs):
                    return function(*args, **kwargs)

                cls.__search__[key] = inner_wrapper
                return inner_wrapper

            return wrapper
        else:
            return cls.__search__[key]
