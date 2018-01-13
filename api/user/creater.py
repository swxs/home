# -*- coding: utf-8 -*-

from hashlib import md5
from bson import ObjectId
from mongoengine.errors import *
import settings
from const import undefined
from models import User
from collections import Collections
from common.Decorator.mem_cache import memorize
from common.Exceptions.ExistException import ExistException
from common.Exceptions.NotExistException import NotExistException


class Creater(object):
    def __new__(cls):
        singleton = cls.__dict__.get('__singleton__')
        if singleton is not None:
            return singleton
        cls.__singleton__ = singleton = object.__new__(cls)
        return singleton

    @classmethod
    def create_user(cls, **kwargs):
        user = User()
        for attr in user.__attrs__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                if attr == "password":
                    value = md5(settings.SECRET_KEY + attr).hexdigest()
                user.__setattr__(attr, value)
        try:
            user.save()
        except NotUniqueError:
            raise ExistException("User")
        return user

    @classmethod
    def refresh(cls, user):
        cls.get_user_by_user_id(user.oid, refresh=1)

    @classmethod
    @memorize
    def get_user_by_user_id(cls, user_id):
        try:
            _id = ObjectId(user_id)
            return User.objects.get(id=_id)
        except User.DoesNotExist:
            raise NotExistException("User")

    @classmethod
    @memorize
    def has_user_by_user_id(cls, user_id):
        try:
            if Creater.get_user_by_user_id(user_id):
                return True
            else:
                return False
        except NotExistException:
            return False

    @classmethod
    def get_user_list(cls):
        return Collections(User.objects.filter())
