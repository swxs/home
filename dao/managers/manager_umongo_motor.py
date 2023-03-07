# -*- coding: utf-8 -*-
# @File    : manager_umongo_motor.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import asyncio
import logging
from collections import defaultdict

from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError
from umongo.frameworks import MotorAsyncIOInstance
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# 通用方法
from commons.Metaclass.Singleton import Singleton

# 本模块方法
from ..fields import DictField
from .manager_base import BaseManager, BaseManagerQuerySet

logger = logging.getLogger("main.dao.manager.manager_umongo_motor")

NAME_DICT = defaultdict(dict)


class ManagerQuerySet(BaseManagerQuerySet):
    def order_by(self, keys):
        if keys:
            key_list = []
            for key in keys:
                if key.startswith("-"):
                    key_list.append((key[1:], DESCENDING))
                else:
                    key_list.append((key, ASCENDING))
            self.cursor.sort(key_list)
        return self

    def __iter__(self):
        if self.cursor is None:
            return list()
        else:
            return self.cursor

    def __next__(self, cursor):
        return self.get_instance(cursor)

    async def __aiter__(self):
        if self.cursor is None:
            yield []
        else:
            async for cursor in self.cursor:
                yield self.get_instance(cursor)

    async def __anext__(self):
        return await self.get_instance(self.cursor)

    async def to_list(self):
        result_list = []
        async for instance in self:
            result_list.append(instance)
        return result_list

    async def to_dict(self):
        result_list = []
        async for instance in self:
            result_list.append(instance.to_dict())
        return result_list

    async def first(self):
        first_model = self.cursor.to_list(1)
        if isinstance(first_model, asyncio.Future):
            first_model = await first_model
        return self.get_instance(first_model)

    async def get_pagination(self):
        return {}


class UmongoMotorManager(BaseManager):
    name = "umongo_motor"

    def get_instance(self, model):
        if model is None:
            return None
        data = dict()
        for attr in getattr(self.dao, "__fields__"):
            data[attr] = getattr(model, attr)
        data["id"] = getattr(model, "id")
        return self.dao(**data)

    async def count(self, finds):
        try:
            return await self.model.count_documents(finds)
        except Exception as e:
            logging.exception(f"count failed! finds = {finds}")
            return None

    async def find_one(self, finds):
        try:
            model = await self.model.find_one(finds)
            return self.get_instance(model)
        except Exception as e:
            logging.exception(f"find_one failed! finds = {finds}")
            return None

    async def find_many(self, finds, limit=0, skip=0):
        try:
            cursor = self.model.find(finds).limit(limit).skip(skip)
            return ManagerQuerySet(self.get_instance, cursor)
        except Exception as e:
            logging.exception(f"find_many failed! finds = {finds}")
            return []

    async def create(self, params):
        try:
            model = self.model()
            for __field_name, __field in getattr(self.dao, "__fields__").items():
                v = params.get(__field_name, __field.create_default)
                if v is not None:
                    setattr(model, __field_name, v)
            await model.commit()
            return self.get_instance(model)
        except Exception as e:
            logging.exception(f"create failed! params = {params}")
            return None

    async def update_one(self, finds, params):
        try:
            model = await self.model.find_one(finds)
            for __field_name, __field in getattr(self.dao, "__fields__").items():
                if __field.default_update:
                    setattr(model, __field_name, __field.update_default)
                if __field_name in params:
                    setattr(model, __field_name, params.get(__field_name))
            await model.commit()
            return self.get_instance(model)
        except Exception as e:
            logging.exception(f"update_one failed! finds = {finds}, params = {params}")
            return None

    async def delete_one(self, finds):
        try:
            model = await self.model.find_one(finds)
            delete_result = await model.delete()
            return delete_result.deleted_count
        except Exception as e:
            logging.exception(f"delete_one failed! finds = {finds}")
            return 0
