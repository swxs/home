# -*- coding: utf-8 -*-
# @File    : manager_mongoenginee.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

from mongoengine import (NotUniqueError, DoesNotExist)
from api import models
from api.consts.const import undefined
from common.Metaclass.Singleton import Singleton
from common.Exceptions import *


class ManagerQuerySet(object):
    def __init__(self, get_instance, model):
        self.get_instance = get_instance
        self.model = model

    def __len__(self):
        return self.model.count()

    def __iter__(self):
        if self.model is None:
            return list()
        else:
            return map(self.get_instance, self.model)

    def first(self):
        return self.get_instance(self.model.first())

    def count(self):
        return self.model.count()


class Manager(object):
    __metaclass__ = Singleton

    def __init__(self):
        pass

    @classmethod
    def _get_model(cls, model_class):
        return models.__dict__[model_class.__model_name__]

    @classmethod
    def _save(cls, model):
        try:
            model.save()
        except NotUniqueError:
            raise ExistException(model._class_name)
        except Exception as e:
            raise e

    @classmethod
    # @memorize
    def _delete(cls, model):
        try:
            model.delete()
        except Exception as e:
            raise e

    @classmethod
    def select(cls, model_class, **kwargs):
        try:
            model = cls._get_model(model_class).objects.get(**kwargs)
        except DoesNotExist as e:
            raise NotExistException(f"{model_class.__model_name__}")
        except Exception as e:
            raise e
        return model_class.get_instance(model)

    @classmethod
    def filter(cls, model_class, *args, **kwargs):
        model = cls._get_model(model_class).objects.filter(**kwargs)
        try:
            return ManagerQuerySet(model_class.get_instance, model)
        except Exception as e:
            print(e)

    @classmethod
    def create(cls, model_class, **kwargs):
        model = cls._get_model(model_class)()
        for attr in model_class.__fields__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                model.__setattr__(attr, value)
        cls._save(model)
        return model_class.get_instance(model)

    @classmethod
    def update(cls, model_class, **kwargs):
        model = cls._get_model(model_class).objects.get(id=model_class.id)
        for attr in model_class.__fields__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                model.__setattr__(attr, value)
        cls._save(model)
        return model_class.get_instance(model)

    @classmethod
    def delete(cls, model_class):
        model = cls._get_model(model_class).objects.get(id=model_class.id)
        cls._delete(model)
