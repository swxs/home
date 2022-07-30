# -*- coding: utf-8 -*-
# @File    : BaseDocument.py
# @AUTH    : swxs
# @Time    : 2018/5/7 22:40

import os
import logging
import hashlib
import datetime
from tkinter import E
from bson import ObjectId
from functools import wraps
from tornado.util import ObjectDict
from .fields import BaseField, DateTimeField, DictField
from .managers import manager_productor
from .memorizers import memorizer_productor

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

        attrs["_manager"] = None
        attrs["_memorizer"] = None

        if attrs.get('Meta'):
            attrs["__model__"] = attrs.get("Meta").model
            attrs["__manager__"] = attrs.get("Meta").manager
            attrs["__memorizer__"] = attrs.get("Meta").memorizer

        current_class = super(BaseMetaDocuemnt, cls).__new__(cls, name, bases, attrs)
        if parent is not None:
            getattr(parent, "__subclass__")[name] = current_class
        return current_class

    @property
    def manager(cls):
        if cls._manager is None:
            cls._manager = manager_productor[cls.__manager__](cls)
        return cls._manager

    @property
    def memorizer(cls):
        if cls._memorizer is None:
            cls._memorizer = memorizer_productor[cls.__memorizer__]()
        return cls._memorizer


class BaseDocument(object, metaclass=BaseMetaDocuemnt):
    metaclass = BaseMetaDocuemnt

    def __init__(self, **kwargs):
        self.id = kwargs.get("_id", None)
        self.oid = kwargs.get("_oid", None)
        self.__raw__ = kwargs.get("__raw__", None)
        self.__fields__ = getattr(self.__class__, "__fields__")
        self.__searches__ = getattr(self.__class__, "__searches__")

        for attr in self.__fields__:
            self.__dict__[attr] = kwargs.get(attr, None)

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
            if self.__getattribute__(field_name) is not None:
                v = self.__getattribute__(field_name)
                if isinstance(v, ObjectId):
                    data[field_name] = str(v)
                else:
                    data[field_name] = v
        return data

    async def to_front(self, dict_factory=ObjectDict):
        try:
            return await self.to_dict(dict_factory=dict_factory)
        except Exception as e:
            print(e)

    @classmethod
    async def find(cls, finds, limit=0, skip=0):
        logger.info(f"[select] <{cls.__model_name__}>: finds - {finds}")

        if not isinstance(finds, dict):
            finds = {"_id": finds}
            return await cls.manager.find_one(finds, limit=limit, skip=skip)
        else:
            return await cls.manager.find_many(finds, limit=limit, skip=skip)

    @classmethod
    async def count(cls, finds):
        try:
            return await cls.manager.count(finds)
        except Exception as e:
            logger.info(e)
            return 0

    @classmethod
    async def is_exist(cls, finds):
        ret = await cls.count(finds)
        return ret > 0

    @classmethod
    async def search(cls, searches, limit=0, skip=0):
        logger.info(f"[search] <{cls.__model_name__}>: searches - {searches}")

        key = cls.get_key_with_params(searches)
        if key in getattr(cls, "__searches__"):
            return getattr(cls, "__searches__")[key](searches, limit=limit, skip=skip)
        else:
            # 没有找到追加规则会退化到find
            return cls.find(searches, limit=limit, skip=skip)

    @classmethod
    async def create(cls, params):
        logger.info(f"[create] <{cls.__model_name__}>: params - {params}")

        try:
            return await cls.manager.create(params)
        except Exception as e:
            raise e

    @classmethod
    async def update(cls, finds, params):
        logger.info(f"[update] <{cls.__model_name__}>: finds - {finds}; params - {params}")

        if not isinstance(finds, dict):
            finds = {"_id": finds}
            return await cls.manager.find_one_and_update(finds, params)
        else:
            # 暂不支持
            raise Exception

    @classmethod
    async def copy(cls, finds, params):
        model = cls.find(finds)
        params_ = model.to_dict(updates=params)
        return await cls.update(finds, params_)

    @classmethod
    async def delete(cls, finds):
        logger.info(f"[delete] <{cls.__model_name__}>: finds - {finds}")

        if not isinstance(finds, dict):
            finds = {"_id": finds}
            return await cls.manager.find_one_and_delete(cls, finds)
        else:
            # 暂不支持
            raise Exception

    @classmethod
    def add_search(cls, *keys):
        key = cls.get_key_with_list(list(keys))
        if key not in cls.__searches__:

            def wrapper(function):
                @wraps(function)
                def inner_wrapper(*args, **kwargs):
                    return function(*args, **kwargs)

                cls.__searches__[key] = inner_wrapper
                return inner_wrapper

            return wrapper
        else:
            return cls.__searches__[key]
