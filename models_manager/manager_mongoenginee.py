# -*- coding: utf-8 -*-
# @File    : manager_mongoenginee.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import itertools
from mongoengine import NotUniqueError
from const import undefined
from models.user import User
from common.Exceptions.ExistException import ExistException

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
    def is_select_one(cls, model_class, **kwargs):
        return False

    @classmethod
    def select_single(cls, model, model_class):
        if model is None:
            return None
        kwargs = dict()
        for attr in model_class.__attrs__:
            kwargs[attr] = model.attr
        return model_class(**kwargs)

    @classmethod
    def select_list(cls, model, model_class):
        while model.next():
            kwargs = dict()
            for attr in model_class.__attrs__:
                kwargs[attr] = model.attr
            yield model_class(kwargs)

    @classmethod
    def create(cls, model_name, model_class, **kwargs):
        model = cls.__modules__.get(model_name)()
        for attr in model_class.__attrs__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                model.attr = value
        try:
            model.save()
        except NotUniqueError:
            raise ExistException(model_name)
        return cls.select_single(model, model_class)

    @classmethod
    def select(cls, model_name, model_class, **kwargs):
        if cls.is_select_one(model_class, **kwargs):
            model = cls.__modules__.get(model_name).objects.get(**kwargs)
            return cls.select_single(model, model_class)
        else:
            if kwargs:
                model = cls.__modules__.get(model_name).objects.filter(**kwargs)
                return cls.select_list(model, model_class)
            else:
                model = cls.__modules__.get(model_name).objects.all()
                return cls.select_list(model, model_class)

    @classmethod
    def update(cls, model_name, model_class):
        model = cls.__modules__.get(model_name).objects.get(id=model_class.id)
        for attr in model.__attrs__:
            value = model_class.__dict__.get(attr, undefined)
            if value != undefined:
                model.__updateattr__(attr, value)
        try:
            model.save()
        except NotUniqueError:
            raise ExistException(model_name)
        return cls.select_single(model, model_class)

    @classmethod
    def delete(cls, model_name, model_class):
        model = cls.__modules__.get(model_name).objects.get(id=model_class.id)
        try:
            model.delete()
        except:
            pass
