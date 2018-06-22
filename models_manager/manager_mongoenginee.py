# -*- coding: utf-8 -*-
# @File    : manager_mongoenginee.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import itertools
from mongoengine import NotUniqueError
from const import undefined
from models.user import User
from common.Exceptions.ExistException import ExistException
from common.Exceptions.DeleteInhibitException import DeleteInhibitException


class Manager(object):
    __modules__ = {
        "User": User
    }

    def __new__(cls, *args):
        singleton = cls.__dict__.get('__singleton__')
        if singleton is not None:
            return singleton
        cls.__singleton__ = singleton = object.__new__(cls)
        return singleton

    def __init__(self):
        pass

    @classmethod
    def _get_model(cls, model_name):
        return cls.__modules__.get(model_name)

    @classmethod
    def select(cls, model_name, model_class, **kwargs):
        model = cls._get_model(model_name).objects.get(**kwargs)
        return model_class.get_instance(model)

    @classmethod
    def filter(cls, model_name, model_class, **kwargs):
        model = cls._get_model(model_name).objects.filter(**kwargs)
        return map(model_class.get_instance, model)


    @classmethod
    def create(cls, model_name, model_class, **kwargs):
        model = cls._get_model(model_name)()
        for attr in model_class.__attrs__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                model.__setattr__(attr, value)
        try:
            model.save()
        except NotUniqueError:
            raise ExistException(model_name)
        return cls.select(model, model_class)

    @classmethod
    def update(cls, model_name, model_class, **kwargs):
        model = cls._get_model(model_name).objects.get(id=model_class.id)
        for attr in model_class.__attrs__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                model.__setattr__(attr, value)
        try:
            model.save()
        except NotUniqueError:
            raise ExistException(model_name)
        return model_class.get_instance(model)

    @classmethod
    def delete(cls, model_name, model_class):
        model = cls._get_model(model_name).objects.get(id=model_class.id)
        try:
            model.delete()
        except:
            raise DeleteInhibitException()
