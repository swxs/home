# -*- coding: utf-8 -*-
# @File    : manager_mongoenginee.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

from mongoengine import NotUniqueError

import models
# from common.Decorator.mem_cache import memorize
from const import undefined
from common.Metaclass.Singleton import Singleton
from common.Exceptions.ExistException import ExistException
from common.Exceptions.DeleteInhibitException import DeleteInhibitException


class Manager(object):
    __metaclass__ = Singleton

    def __init__(self):
        pass

    @classmethod
    def _get_model(cls, model_class):
        return models.__dict__[model_class.__model_name__]

    @classmethod
    # @memorize
    def _save(cls, model):
        try:
            model.save()
        except NotUniqueError:
            raise ExistException(model._class_name)

    @classmethod
    # @memorize
    def _delete(cls, model):
        try:
            model.delete()
        except DeleteInhibitException:
            raise DeleteInhibitException(model._class_name)

    @classmethod
    # @memorize
    def select(cls, model_class, **kwargs):
        '''
        TODO:  这里需要建立缓存（结果）， 一份缓存多次使用， 主要是id的， 其他映射到id上
        '''
        model = cls._get_model(model_class).objects.get(**kwargs)
        return model_class.get_instance(model)

    @classmethod
    def filter(cls, model_class, **kwargs):
        model = cls._get_model(model_class).objects.filter(**kwargs)
        try:
            return map(model_class.get_instance, model)
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
        '''
        保存修改前的原值， 修改失败则复原？
        :param model_class:
        :param kwargs:
        :return:
        '''
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
