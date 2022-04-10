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
    def __iter__(self):
        if self.cursor is None:
            return list()
        else:
            return self.cursor

    def __next__(self, cursor):
        return self.get_instance(cursor, filters=self.filters)

    async def __aiter__(self):
        if self.cursor is None:
            yield []
        else:
            async for cursor in self.cursor:
                yield self.get_instance(cursor, filters=self.filters)

    async def __anext__(self):
        return await self.get_instance(self.cursor, filters=self.filters)

    async def to_list(self):
        result_list = []
        async for instance in self:
            result_list.append(instance)
        return result_list

    async def first(self):
        first_model = self.cursor.to_list(1)
        if isinstance(first_model, asyncio.Future):
            first_model = await first_model
        return self.get_instance(first_model, filters=self.filters)

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


class UmongoMotorManager(BaseManager):
    name = "umongo_motor"

    def __init__(self, dao) -> None:
        super().__init__(dao)
        self.dao = dao
        self.model = dao.__model__

    async def find_one(self, finds, limit=0, skip=0):
        try:
            model = await self.model.find(finds)
        except Exception as e:
            logging.warning(f"find failed with {finds}")
            raise e
        return self.dao.get_instance(model)

    async def find_many(self, finds, limit=0, skip=0):
        try:
            model = await self.model.search(finds).limit(limit).skip(skip)
        except Exception as e:
            logging.warning(f"find failed with {finds}")
            raise e
        return ManagerQuerySet(model, self.dao.get_instance)

    async def count(self, finds):
        try:
            return await self.model.count_documents(finds)
        except Exception as e:
            raise e

    async def create(self, params):
        model = self.model()
        for attr in self.dao.__fields__:
            model.__setattr__(attr, params.get(attr))
        try:
            await model.commit()
        # except (DuplicateKeyError,) as e:
        #     raise ApiException(Info.Existed, message=self.model.__name__)
        except Exception as e:
            raise e
        return self.dao.get_instance(model)

    async def find_one_and_update(self, finds, params):
        instance = await self.find(finds)
        model = instance.__raw__
        for attr in self.dao.__fields__:
            model.__setattr__(attr, params.get(attr, getattr(instance, attr)))

        try:
            await model.commit()
        # except (DuplicateKeyError,) as e:
        #     raise ApiException(Info.Existed, message=self.model.__name__)
        except Exception as e:
            raise e
        return self.dao.get_instance(model)

    async def find_one_and_delete(self, finds):
        instance = await self.find_one(finds)
        model = instance.__raw__
        try:
            delete_result = await model.delete()
            return delete_result.deleted_count
        except Exception as e:
            raise e
