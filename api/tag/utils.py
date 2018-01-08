# -*- coding: utf-8 -*-

import datetime
from mongoengine.errors import *
from bson import ObjectId
from const import undefined
import enums as enums
import models as models
from common.Decorator.mem_cache import memorize
from common.Exceptions.ExistException import ExistException
from common.Exceptions.NotExistException import NotExistException

def refresh(tag):
    get_tag_by_tag_id(tag.oid, refresh=1)


@memorize
def get_tag_by_tag_id(tag_id):
    try:
        _id = ObjectId(tag_id)
        return models.Tag.objects.get(id=_id)
    except models.Tag.DoesNotExist:
        raise NotExistException("Tag")


@memorize
def has_tag_by_tag_id(tag_id):
    try:
        if get_tag_by_tag_id(tag_id):
            return True
        else:
            return False
    except NotExistException:
        return False


def get_tag_list():
    return models.Tag.objects.filter()


def create(**kwargs):
    tag = models.Tag()
    for attr in tag.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            tag.__setattr__(attr, value)
    try:
        tag.save()
    except NotUniqueError:
        raise ExistException("Tag")
    return tag


def update(tag, **kwargs):
    for attr in tag.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            tag.__setattr__(attr, value)
    tag.updated = datetime.datetime.now()
    try:
        tag.save()
    except NotUniqueError:
        raise ExistException("Tag")
    refresh(tag)
    return tag


def delete(tag):
    tag.delete()
    refresh(tag)
    return None


def to_front(tag):
    if tag:
        return tag.to_dict()
