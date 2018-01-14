# -*- coding: utf-8 -*-

from hashlib import md5
from bson import ObjectId
from mongoengine.errors import *
import settings
from const import undefined
from models import PasswordLock
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
    def create_password_lock(cls, **kwargs):
        password_lock = PasswordLock()
        for attr in password_lock.__attrs__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                if attr == "name":
                    password_lock.__updateattr__("key", value)
                password_lock.__updateattr__(attr, value)
        try:
            password_lock.save()
        except NotUniqueError:
            raise ExistException("PasswordLock")
        return password_lock

    @classmethod
    def refresh(cls, password_lock):
        cls.get_password_lock_by_password_lock_id(password_lock.oid, refresh=1)
        cls.get_password_lock_by_password_lock_id_user_id(password_lock.oid, password_lock.user_id, refresh=1)

    @classmethod
    @memorize
    def get_password_lock_by_password_lock_id(cls, password_lock_id):
        try:
            _id = ObjectId(password_lock_id)
            return PasswordLock.objects.get(id=_id)
        except PasswordLock.DoesNotExist:
            raise NotExistException("PasswordLock")

    @classmethod
    @memorize
    def get_password_lock_by_password_lock_id_user_id(cls, password_lock_id, user_id):
        try:
            _id = ObjectId(password_lock_id)
            return PasswordLock.objects.get(id=_id, user_id=user_id)
        except PasswordLock.DoesNotExist:
            raise NotExistException("PasswordLock")

    @classmethod
    @memorize
    def has_password_lock_by_password_lock_id(cls, password_lock_id):
        try:
            if Creater.get_password_lock_by_password_lock_id(password_lock_id):
                return True
            else:
                return False
        except NotExistException:
            return False

    @classmethod
    def get_password_lock_list(cls):
        return Collections(PasswordLock.objects.all())

    @classmethod
    def get_password_lock_list_by_user_id(cls, user_id):
        return Collections(PasswordLock.objects.filter(user_id=user_id))
