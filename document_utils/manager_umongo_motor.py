# -*- coding: utf-8 -*-
# @File    : manager_umongo_motor.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import asyncio
from bson import ObjectId
from async_property import async_property
from mongoengine import (NotUniqueError, ValidationError, DoesNotExist)
from pymongo.errors import (DuplicateKeyError, )
from api.BaseConsts import undefined
from .models_fields import DictField
from common.Metaclass.Singleton import Singleton
from common.Utils.log_utils import getLogger

NAME_DICT = {}

log = getLogger("manager.manager_umongo_motor")


class ManagerQuerySet(object):
    def __init__(self, get_instance, model):
        """
        :param get_instance: 转换为对应类的方法
        :param model: cursor
        """
        self.get_instance = get_instance
        self.model = model
        self._filter = dict()

    def __iter__(self):
        if self.model is None:
            return list()
        else:
            return map(lambda model: self.get_instance(model, _filter=self._filter), self.model)

    async def __aiter__(self):
        if self.model is None:
            yield []
        else:
            async for model in self.model:
                yield self.get_instance(model, _filter=self._filter)

    async def first(self):
        first_model = self.model.to_list(1)
        if isinstance(first_model, asyncio.Future):
            first_model = await first_model
        return self.get_instance(first_model, _filter=self._filter)

    async def order_by(self, key_list):
        """
        返回排序后的数据
        :param key_list: [('key1', 1/-1), ('key1', 1/-1)]
        :return:
        """
        self.model = self.model.sort(key_list)

        return self


class Manager(object):
    __metaclass__ = Singleton

    def __init__(self):
        pass

    @classmethod
    def _get_model(cls, model_class):
        return NAME_DICT[model_class.__model_name__]

    @classmethod
    async def _save(cls, model):
        try:
            await model.commit()
        except ValidationError as e:
            raise ApiValidateException(model.__class__.__name__)
        except (NotUniqueError, DuplicateKeyError) as e:
            raise ApiExistException(model.__class__.__name__)
        except Exception as e:
            raise e

    @classmethod
    async def _delete(cls, model):
        try:
            await model.delete()
        except Exception as e:
            raise e

    @classmethod
    async def count(cls, model_class, **kwargs):
        try:
            return await cls._get_model(model_class).count_documents(**kwargs)
        except Exception as e:
            raise e

    @classmethod
    async def select(cls, model_class, **kwargs):
        try:
            model = await cls._get_model(model_class).find_one(kwargs)
        except DoesNotExist:
            raise ApiNotExistException(f"{model_class.__model_name__}")
        except Exception as e:
            raise e
        return model_class.get_instance(model)

    @classmethod
    def filter(cls, model_class, **kwargs):
        model = cls._get_model(model_class).find(**kwargs)
        try:
            return ManagerQuerySet(model_class.get_instance, model)
        except Exception as e:
            print(e)

    @classmethod
    async def create(cls, model_class, **kwargs):
        model = cls._get_model(model_class)()
        for attr in model_class.__fields__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                model.__setattr__(attr, value)
        await cls._save(model)
        return model_class.get_instance(model)

    @classmethod
    async def update(cls, model_class, **kwargs):
        model = model_class.__raw_model__
        for attr in model_class.__fields__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                if isinstance(model_class.__fields__[attr], DictField):
                    model.__getitem__(attr).update(value)
                    model.__setattr__(attr, model.__getitem__(attr))
                else:
                    model.__setattr__(attr, value)
        await cls._save(model)
        return model_class.get_instance(model)

    @classmethod
    async def delete(cls, model_class):
        model = await cls._get_model(model_class).find_one({"_id": model_class.oid})
        await cls._delete(model)
