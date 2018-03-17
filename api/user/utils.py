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
from api.user.models import User


def refresh(user):
    get_user_by_user_id(user.oid, refresh=1)


def create_user(**kwargs):
    user = User()
    for attr in user.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            user.__updateattr__(attr, value)
    try:
        user.save()
    except NotUniqueError:
        raise ExistException("User")
    return user


@memorize
def get_user_by_user_id(user_id):
    try:
        _id = ObjectId(user_id)
        return User.objects.get(id=_id)
    except User.DoesNotExist:
        raise NotExistException("User")


def get_user_list():
    return User.objects.all()


def update_user(user, **kwargs):
    for attr in user.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            user.__updateattr__(attr, value)
    user.updated = datetime.datetime.now()
    try:
        user.save()
    except NotUniqueError:
        raise ExistException("User")
    refresh(user)
    return user


def delete_user(user):
    user.delete()
    refresh(user)
    return None


def to_front(user):
    d = json.loads(user.to_json())
    d['id'] = user.oid
    d.pop('_id')
    return ObjectDict(d)
