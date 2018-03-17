# -*- coding: utf-8 -*-

import json
import datetime
from bson import ObjectId
from tornado.util import ObjectDict
from mongoengine.errors import NotUniqueError
import settings
from const import undefined
from common.Decorator.mem_cache import memorize
from common.Exceptions.ExistException import ExistException
from common.Exceptions.NotExistException import NotExistException
from common.Exceptions.ValidateException import ValidateException
from api.password_lock.models import PasswordLock


def refresh(password_lock):
    get_password_lock_by_password_lock_id(password_lock.oid, refresh=1)
    get_password_lock_by_password_lock_id_user_id(password_lock.oid, password_lock.user_id, refresh=1)


def create_password_lock(**kwargs):
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


@memorize
def get_password_lock_by_password_lock_id(password_lock_id):
    try:
        _id = ObjectId(password_lock_id)
        return PasswordLock.objects.get(id=_id)
    except PasswordLock.DoesNotExist:
        raise NotExistException("PasswordLock")


@memorize
def get_password_lock_by_password_lock_id_user_id(password_lock_id, user_id):
    try:
        _id = ObjectId(password_lock_id)
        return PasswordLock.objects.get(id=_id, user_id=user_id)
    except PasswordLock.DoesNotExist:
        raise NotExistException("PasswordLock")


def get_password_lock_list():
    return PasswordLock.objects.all()


def get_password_lock_list_by_user_id(cls, user_id):
    return PasswordLock.objects.filter(user_id=user_id)


def update_password_lock(password_lock, **kwargs):
    for attr in password_lock.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            password_lock.__updateattr__(attr, value)
    password_lock.updated = datetime.datetime.now()
    try:
        password_lock.save()
    except NotUniqueError:
        raise ExistException("PasswordLock")
    refresh(password_lock)
    return password_lock


def delete_password_lock(password_lock):
    password_lock.delete()
    refresh(password_lock)
    return None


def to_front(password_lock):
    d = json.loads(password_lock.to_json())
    d['id'] = password_lock.oid
    d['password'] = password_lock.password
    d.pop('_id')
    return ObjectDict(d)
