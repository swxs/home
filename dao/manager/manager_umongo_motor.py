# -*- coding: utf-8 -*-
# @File    : manager_umongo_motor.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import asyncio
from collections import defaultdict
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import (DuplicateKeyError, )
from mongoengine import (NotUniqueError, ValidationError, DoesNotExist)
from web.consts import undefined
from web.exceptions import ApiException, Info
from ..fields import DictField
from .manager_base import BaseManager, BaseManagerQuerySet
from common.Metaclass.Singleton import Singleton
from common.Utils.log_utils import getLogger

log = getLogger("manager.manager_umongo_motor")

NAME_DICT = defaultdict(dict)

class ManagerQuerySet(BaseManagerQuerySet):
    def __iter__(self):
        if self.cursor is None:
            return list()
        else:
            return self.cursor

    def __next__(self, cursor):
        return self.get_instance(cursor, _filter=self._filter)

    async def __aiter__(self):
        if self.cursor is None:
            yield []
        else:
            async for cursor in self.cursor:
                yield self.get_instance(cursor, _filter=self._filter)

    async def __anext__(self, cursor):
        return await self.get_instance(cursor, _filter=self._filter)

    async def first(self):
        first_model = self.cursor.to_list(1)
        if isinstance(first_model, asyncio.Future):
            first_model = await first_model
        return self.get_instance(first_model, _filter=self._filter)

    def order_by(self, key_or_list):
        if key_or_list:
            key_list = []
            for key in key_or_list:
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
        except ValidationError as e:
            raise ApiException(Info.ParamsValidate, message=model.__class__.__name__)
        except (NotUniqueError, DuplicateKeyError) as e:
            raise ApiException(Info.Existed, message=model.__class__.__name__)
        except Exception as e:
            raise e

    @classmethod
    async def _delete(cls, model):
        try:
            await model.delete()
        except Exception as e:
            raise e

    @classmethod
    async def count(cls, klass, **kwargs):
        try:
            return await cls._get_model(klass).count_documents(**kwargs)
        except Exception as e:
            raise e

    @classmethod
    async def select(cls, klass, **kwargs):
        try:
            model = await cls._get_model(klass).find_one(kwargs)
        except DoesNotExist:
            raise ApiException(Info.NotExist, message=klass.__name__)
        except Exception as e:
            raise e
        if model is None:
            raise ApiException(Info.NotExist, message=klass.__name__)
        return klass.get_instance(model)

    @classmethod
    def filter(cls, klass, **kwargs):
        limit = kwargs.pop('limit', 0)
        skip = kwargs.pop('skip', 0)
        model = cls._get_model(klass).find(kwargs, limit=limit, skip=skip)
        try:
            return ManagerQuerySet(klass.get_instance, model)
        except Exception as e:
            print(e)

    @classmethod
    async def create(cls, klass, **kwargs):
        model = cls._get_model(klass)()
        for attr in klass.__fields__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                model.__setattr__(attr, value)
        await cls._save(model)
        return klass.get_instance(model)

    @classmethod
    async def update(cls, klass, instance, **kwargs):
        model = instance.__raw_model__
        for attr in klass.__fields__:
            value = kwargs.get(attr, undefined)
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
        model = await cls._get_model(klass).find_one({"_id": instance.oid})
        return await cls._delete(model)
