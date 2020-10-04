# -*- coding: utf-8 -*-
# @File    : BaseDocument.py
# @AUTH    : swxs
# @Time    : 2018/5/7 22:40

import os
import logging
import hashlib
import datetime
from bson import ObjectId
from functools import wraps
from tornado.util import ObjectDict

import settings
from web import undefined
from .fields import BaseField, DateTimeField, DictField
from .manager_productor import manager_productor
from .memorizer.memorizer_cache import clear, upgrade, cache

logger = logging.getLogger("main.dao.base_document")


class BaseMetaDocuemnt(type):
    """
    简介
    ----------


    参数
    ----------
    type :

    """

    def __new__(cls, name, bases, attrs):
        __fields__ = {}

        parent = None
        for base in bases:
            if isinstance(base, cls) and (getattr(base, "__model_name__") != 'BaseDocument'):
                parent = base
                for key, value in base.__fields__.items():
                    __fields__[key] = value

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, BaseField):
                attr_value.name = attr_name
                __fields__[attr_name] = attr_value

        attrs["__fields__"] = __fields__
        attrs["__searches__"] = dict()  # 记录搜索的方法字段
        attrs["__subclass__"] = dict()  # 记录子类
        attrs["__model_name__"] = name  # 记录model的名称
        if 'meta' in attrs:
            meta_data: dict = attrs.get('meta', {})
            attrs["__base_model_name__"] = meta_data.get('inheritance', name)
        else:
            attrs["__base_model_name__"] = name

        current_class = super(BaseMetaDocuemnt, cls).__new__(cls, name, bases, attrs)
        if parent is not None:
            getattr(parent, "__subclass__")[name] = current_class
        return current_class

    @property
    def manager(cls):
        return manager_productor[cls.__manager__]


class BaseDocument(object, metaclass=BaseMetaDocuemnt):
    metaclass = BaseMetaDocuemnt

    def __init__(self, **kwargs):
        self.id = kwargs.get("_id", undefined)
        self.oid = kwargs.get("_oid", undefined)
        self.__raw__ = kwargs.get("__raw__", undefined)
        self.__fields__ = getattr(self.__class__, "__fields__")
        self.__searches__ = getattr(self.__class__, "__searches__")

        for attr in self.__fields__:
            self.__dict__[attr] = kwargs.get(attr, undefined)

        self._data = {}
        for key, value in kwargs.items():
            self._data[key] = value

    @classmethod
    def schema(cls):
        return getattr(cls, "__raw__").schema.as_marshmallow_schema()()

    @classmethod
    def get_key_with_list(cls, params):
        params.sort()
        return hashlib.md5(b"".join(p.encode("utf8") for p in params)).hexdigest()

    @classmethod
    def get_key_with_params(cls, params: dict = None):
        return cls.get_key_with_list(list(params.keys()))

    @classmethod
    def get_instance(cls, model, filters=None):
        filters = dict() if filters is None else filters

        data = dict()
        if "only" in filters:
            all_fields = filters["only"]
        else:
            all_fields = getattr(cls, "__fields__")

        for attr in all_fields:
            if attr not in filters.get("exclude", []):
                data[attr] = getattr(model, attr)

        data["_id"] = str(getattr(model, "id"))
        data["_oid"] = getattr(model, "id")
        data["__raw__"] = model
        return cls(**data)

    async def to_dict(self, dict_factory=ObjectDict):
        data = dict_factory()
        data["id"] = self.__dict__["id"]
        for field_name in self.__fields__:
            if self.__getattribute__(field_name) != undefined:
                data[field_name] = self.__getattribute__(field_name)
        return data

    async def to_front(self, dict_factory=ObjectDict):
        return await self.to_dict(dict_factory=dict_factory)

    @classmethod
    # @cache
    async def find(cls, finds: dict):
        if "id" in finds:
            finds["_id"] = ObjectId(finds.pop("id"))
        logger.info(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [select] <{getattr(cls, '__model_name__')}>: kwargs - {str(finds)}"
        )
        return await cls.manager.find(cls, finds)

    @classmethod
    async def is_exist(cls, finds: dict):
        try:
            await cls.find(finds)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    @classmethod
    def search(cls, searches, limit=0, skip=0):
        logger.info(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [search] <{getattr(cls, '__model_name__')}>: kwargs - {str(searches)}"
        )
        key = cls.get_key_with_params(searches)
        if key in getattr(cls, "__searches__"):
            return getattr(cls, "__searches__")[key](cls, searches)
        else:
            return cls.manager.search(cls, searches, limit=limit, skip=skip)

    @classmethod
    async def count(cls, searches):
        try:
            return await cls.manager.count(cls, searches)
        except Exception as e:
            logger.exception(e)
            return 0

    @classmethod
    async def create(cls, creates: dict):
        logger.info(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [create] <{getattr(cls, '__model_name__')}>: kwargs - {str(creates)}"
        )
        return await cls.manager.create(cls, creates)

    async def copy(self, copies):
        params = await self.to_dict()
        for attr in self.__fields__:
            value = copies.get(attr, undefined)
            if value != undefined:
                if isinstance(self.__fields__[attr], DictField):
                    params[attr].update(value)
                else:
                    params[attr] = value
        return await self.__class__.create(params)

    @classmethod
    async def find_and_copy(cls, finds: dict, copies: dict):
        if "id" in finds:
            finds["_id"] = ObjectId(finds.pop("id"))
        instance = await cls.find(finds)
        return await instance.copy(copies)

    async def update(self, updates: dict):
        logger.info(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [update] <{getattr(self, '__model_name__')}>: finds - {str(dict(id=self.id))}; updates - {str(updates)}"
        )
        return await self.__class__.manager.update(self.__class__, self, updates)

    @classmethod
    async def find_and_update(cls, finds: dict, updates: dict):
        if "id" in finds:
            finds["_id"] = ObjectId(finds.pop("id"))
        logger.info(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [update] <{getattr(cls, '__model_name__')}>: finds - {str(finds)}; updates - {str(updates)}"
        )
        return await cls.manager.find_and_update(cls, finds, updates)

    @classmethod
    async def search_and_update(cls, searches: dict, updates: dict):
        logger.info(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [update] <{getattr(cls, '__model_name__')}>: searches - {str(searches)}; updates - {str(updates)}"
        )
        return await cls.manager.searches_and_update(cls, searches, updates)

    async def delete(self):
        logger.info(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [delete] <{getattr(self, '__model_name__')}>: finds - {str(dict(id=self.id))}"
        )
        return await self.__class__.manager.delete(self.__class__, self)

    @classmethod
    async def find_and_delete(cls, finds: dict):
        if "id" in finds:
            finds["_id"] = ObjectId(finds.pop("id"))
        logger.info(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [delete] <{getattr(cls, '__model_name__')}>: finds - {str(finds)}"
        )
        return await cls.manager.find_and_delete(cls, finds)

    @classmethod
    async def search_and_delete(cls, searches: dict):
        logger.info(
            f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S:%f} [delete] <{getattr(cls, '__model_name__')}>: searches - {str(searches)}"
        )
        return await cls.manager.searches_and_delete(cls, searches)

    @classmethod
    def add_search(cls, *args):
        key = cls.get_key_with_list(list(args))
        if key not in getattr(cls, "__searches__"):

            def wrapper(function):
                @wraps(function)
                def inner_wrapper(*args, **kwargs):
                    return function(*args, **kwargs)

                getattr(cls, "__searches__")[key] = inner_wrapper
                return inner_wrapper

            return wrapper
        else:
            return getattr(cls, "__searches__")[key]
