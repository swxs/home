# -*- coding: utf-8 -*-
# @File    : manager_umongo_motor.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import logging
import asyncio
from collections import defaultdict
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import (
    DuplicateKeyError,
)
from web import ApiException, Info, undefined
from commons.Metaclass.Singleton import Singleton
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


class Manager(BaseManager, metaclass=Singleton):
    name = "umongo_motor"

    @classmethod
    def _get_model(cls, klass):
        return NAME_DICT[klass.__name__]

    @classmethod
    async def _save(cls, model):
        try:
            return await model.commit()
        # except ValidationError as e:
        #     raise ApiException(Info.ParamsValidate, message=model.__class__.__name__)
        except (DuplicateKeyError,) as e:
            raise ApiException(Info.Existed, message=model.__class__.__name__)
        except Exception as e:
            raise e

    @classmethod
    async def _delete(cls, model):
        try:
            delete_result = await model.delete()
            return delete_result.deleted_count
        except Exception as e:
            raise e

    @classmethod
    async def count(cls, klass, searches):
        try:
            return await cls._get_model(klass).count_documents(searches)
        except Exception as e:
            raise e

    @classmethod
    async def find(cls, klass, finds):
        try:
            model = await cls._get_model(klass).find_one(finds)
        # except DoesNotExist:
        #     raise ApiException(Info.NotExist, message=klass.__name__)
        except Exception as e:
            raise e
        if model is None:
            raise ApiException(Info.NotExist, message=klass.__name__)
        return klass.get_instance(model)

    @classmethod
    def search(cls, klass, searches, limit=0, skip=0):
        model = cls._get_model(klass).find(searches, limit=limit, skip=skip)
        try:
            return ManagerQuerySet(klass.get_instance, model)
        except Exception as e:
            logger.exception(e)

    @classmethod
    async def create(cls, klass, creates):
        model = cls._get_model(klass)()
        for attr in klass.__fields__:
            value = creates.get(attr, undefined)
            if value != undefined:
                model.__setattr__(attr, value)
        await cls._save(model)
        return klass.get_instance(model)

    @classmethod
    async def update(cls, klass, instance, updates):
        model = instance.__raw__
        for attr in klass.__fields__:
            value = updates.get(attr, undefined)
            if value != undefined:
                if isinstance(klass.__fields__[attr], DictField):
                    model.__getitem__(attr).update(value)
                    model.__setattr__(attr, model.__getitem__(attr))
                else:
                    model.__setattr__(attr, value)
        await cls._save(model)
        return klass.get_instance(model)

    @classmethod
    async def find_and_update(cls, klass, finds, updates):
        instance = await cls.find(klass, finds)
        model = instance.__raw__
        for attr in klass.__fields__:
            value = updates.get(attr, undefined)
            if value != undefined:
                if isinstance(klass.__fields__[attr], DictField):
                    model.__getitem__(attr).update(value)
                    model.__setattr__(attr, model.__getitem__(attr))
                else:
                    model.__setattr__(attr, value)
        await cls._save(model)
        return klass.get_instance(model)

    @classmethod
    async def delete(cls, klass, instance):
        model = instance.__raw__
        return await cls._delete(model)

    @classmethod
    async def find_and_delete(cls, klass, finds):
        instance = await cls.find(klass, finds)
        model = instance.__raw__
        return await cls._delete(model)

    @classmethod
    async def search_and_delete(cls, klass, searches):
        count = 0
        cursor = cls.search(klass, searches)
        async for instance in cursor:
            model = instance.__raw__
            count += await cls._delete(model)
        return count
