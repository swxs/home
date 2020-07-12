# -*- coding: utf-8 -*-
# @File    : manager_sqlalchemy.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import asyncio
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, MetaData, Table
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import sessionmaker
from sqlalchemy_aio import ASYNCIO_STRATEGY, TRIO_STRATEGY
from sqlalchemy_aio.asyncio import AsyncioEngine

import settings
from web.consts import undefined
from web.exceptions import ApiCommonException, CommmonExceptionInfo
from ..fields import DictField
from .manager_base import BaseManager, BaseManagerQuerySet
from common.Metaclass.Singleton import Singleton
from common.Utils.log_utils import getLogger

log = getLogger("manager.manager_sqlalchemy")

Base = declarative_base()

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
    name = "sqlalchemy"
    Session = sessionmaker(bind=settings.engine)

    @classmethod
    def _get_model(cls, klass):
        return NAME_DICT[cls.name][klass.__name__]

    @classmethod
    async def _save(cls, model):
        try:
            session = cls.Session()
            session.add(model)
            return await session.commit()
        except ValidationError as e:
            raise ApiCommonException(CommmonExceptionInfo.ValidateException, message=model.__class__.__name__)
        except (NotUniqueError, DuplicateKeyError) as e:
            raise ApiCommonException(CommmonExceptionInfo.ExistedException, message=model.__class__.__name__)
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
            return await conn.execute(cls._get_model(klass).rowcount(**kwargs))
        except Exception as e:
            raise e

    @classmethod
    async def select(cls, klass, **kwargs):
        try:
            model = await conn.execute(cls._get_model(klass).select(kwargs))
        except DoesNotExist:
            raise ApiCommonException(CommmonExceptionInfo.NotExistException, message=klass.__class__.__name__)
        except Exception as e:
            raise e
        return klass.get_instance(model)

    @classmethod
    def filter(cls, klass, **kwargs):
        model = cls._get_model(klass).select(kwargs)
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
        model = await conn.execute(cls._get_model(klass).select({"_id": instance.oid}))
        return await cls._delete(model)