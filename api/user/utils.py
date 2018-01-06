# -*- coding: utf-8 -*-

import datetime
from mongoengine.errors import *
from bson import ObjectId
from hashlib import md5
from const import undefined
import settings
import enums as enums
import models as models
from common.Decorator.mem_cache import memorize
from common.Exceptions.ExistException import ExistException
from common.Exceptions.NotExistException import NotExistException

def refresh(user):
    get_user_by_user_id(user.oid, refresh=1)


@memorize
def get_user_by_user_id(user_id):
    try:
        _id = ObjectId(user_id)
        return models.User.objects.get(id=_id)
    except models.User.DoesNotExist:
        raise NotExistException("User")


@memorize
def has_user_by_user_id(user_id):
    try:
        if get_user_by_user_id(user_id):
            return True
        else:
            return False
    except NotExistException:
        return False


def get_user_list():
    return models.User.objects.filter()


def create(**kwargs):
    user = models.User()
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


def update(user, **kwargs):
    for attr in user.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            if attr == "password":
                value = md5(settings.SECRET_KEY + attr).hexdigest()
            user.__setattr__(attr, value)
    user.updated = datetime.datetime.now()
    try:
        user.save()
    except NotUniqueError:
        raise ExistException("User")
    refresh(user)
    return user


def delete(user):
    user.delete()
    refresh(user)
    return None


def to_front(user):
    if user:
        return user.to_dict()
