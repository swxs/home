# -*- coding: utf-8 -*-
# @File    : BaseDocument.py
# @AUTH    : swxs
# @Time    : 2018/5/7 22:40

import os
import hashlib
import logging
import datetime
from functools import wraps

from bson import ObjectId
from tornado.util import ObjectDict

# 本模块方法
from .fields import BaseField, DictField, DateTimeField
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

        attrs["_data"] = dict()
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
            cls._memorizer = memorizer_productor[cls.__memorizer__](cls)
        return cls._memorizer


class BaseDocument(object, metaclass=BaseMetaDocuemnt):
    metaclass = BaseMetaDocuemnt

    def __init__(self, **kwargs):
        for __field_name, __field in getattr(self.__class__, "__fields__").items():
            self.__dict__[__field_name] = kwargs.get(__field_name)
            setattr(self, __field_name, kwargs.get(__field_name))

    @classmethod
    def get_key_with_list(cls, params: list):
        return hashlib.md5(b"".join(p.encode("utf8") for p in sorted(params))).hexdigest()

    @classmethod
    def get_key_with_params(cls, params: dict):
        return cls.get_key_with_list(params.keys())

    def to_dict(self, dict_factory=ObjectDict):
        data = dict_factory()
        for __field_name, __field in getattr(self.__class__, "__fields__").items():
            v = self.__getattribute__(__field_name)
            if v is not None:
                data[__field_name] = __field.to_dict(v)
        return data

    @classmethod
    async def count(cls, finds):
        logger.info(f"[count] <{cls.__model_name__}>: finds - {finds}")

        return await cls.manager.count(finds)

    @classmethod
    async def find_one(cls, finds):
        logger.info(f"[find_one] <{cls.__model_name__}>: finds - {finds}")

        return await cls.manager.find_one(finds)

    @classmethod
    async def find_many(cls, finds, *, limit=0, skip=0):
        logger.info(f"[find_many] <{cls.__model_name__}>: finds - {finds}")

        return await cls.manager.find_many(finds, limit=limit, skip=skip)

    @classmethod
    async def search(cls, searches, *, limit=0, skip=0):
        logger.info(f"[search] <{cls.__model_name__}>: searches - {searches}")

        key = cls.get_key_with_params(searches)
        if key in getattr(cls, "__searches__"):
            return getattr(cls, "__searches__")[key](searches, limit=limit, skip=skip)
        else:
            # 没有找到追加规则会退化到find_many
            return await cls.find_many(searches, limit=limit, skip=skip)

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

    @classmethod
    async def create(cls, params: dict):
        logger.info(f"[create] <{cls.__model_name__}>: params - {params}")

        return await cls.manager.create(params)

    @classmethod
    async def update_one(cls, finds: dict, params: dict):
        logger.info(f"[update_one] <{cls.__model_name__}>: finds - {finds}; params - {params}")

        return await cls.manager.update_one(finds, params)

    @classmethod
    async def update_many(cls, finds: dict, params: dict):
        logger.info(f"[update_many] <{cls.__model_name__}>: finds - {finds}; params - {params}")

        return await cls.manager.update_many(finds, params)

    @classmethod
    async def delete_one(cls, finds: dict):
        logger.info(f"[delete_one] <{cls.__model_name__}>: finds - {finds}")

        return await cls.manager.delete_one(cls, finds)

    @classmethod
    async def delete_many(cls, finds: dict):
        logger.info(f"[delete_many] <{cls.__model_name__}>: finds - {finds}")

        return await cls.manager.delete_many(cls, finds)
