# -*- coding: utf-8 -*-
# @File    : manager_mongoenginee.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

from mongoengine import (NotUniqueError, ValidationError, DoesNotExist)
from api.BaseConsts import undefined
from .models_fields import DictField
from common.Metaclass.Singleton import Singleton
from common.Exceptions import *
from common.Utils.log_utils import getLogger

NAME_DICT = {}

log = getLogger("manager.mongoenginee")


class ManagerQuerySet(object):
    def __init__(self, get_instance, model):
        self.get_instance = get_instance
        self.model = model
        self._filter = dict()

    def __len__(self):
        return self.model.count()

    def __iter__(self):
        if self.model is None:
            return list()
        else:
            return map(lambda model: self.get_instance(model, _filter=self._filter), self.model)

    def first(self):
        first_model = self.model.first()
        if first_model is None:
            return None
        else:
            return self.get_instance(first_model, _filter=self._filter)

    def count(self):
        return self.model.count()

    def only(self, *keys):
        if self.model is not None:
            self._filter["only"] = list(keys)
            self.model.only(*keys)
        return self

    def exclude(self, *keys):
        if self.model is not None:
            self._filter["exclude"] = list(keys)
            self.model.exclude(*keys)
        return self

    def order_by(self, *keys):
        if self.model is not None:
            self.model.order_by(*keys)
        return self


class Manager(object):
    __metaclass__ = Singleton

    def __init__(self):
        pass

    @classmethod
    def _get_model(cls, model_class):
        return NAME_DICT[model_class.__model_name__]

    @classmethod
    def _save(cls, model):
        try:
            model.save()
        except ValidationError as e:
            raise ApiValidateException(model._class_name)
        except NotUniqueError:
            raise ApiExistException(model._class_name)
        except Exception as e:
            raise e

    @classmethod
    def _delete(cls, model):
        try:
            model.delete()
        except Exception as e:
            raise e

    @classmethod
    def select(cls, model_class, **kwargs):
        try:
            model = cls._get_model(model_class).objects.get(**kwargs)
        except DoesNotExist:
            raise ApiNotExistException(f"{model_class.__model_name__}")
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
        model = model_class._raw_model
        for attr in model_class.__fields__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                if isinstance(model_class.__fields__[attr], DictField):
                    model.__getitem__(attr).update(value)
                    model.__setattr__(attr, model.__getitem__(attr))
                else:
                    model.__setattr__(attr, value)
        cls._save(model)
        return model_class.update_instance(model)

    @classmethod
    def delete(cls, model_class):
        model = cls._get_model(model_class).objects.get(id=model_class.id)
        cls._delete(model)
