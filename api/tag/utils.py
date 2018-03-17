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
from api.tag.models import Tag


def refresh(tag):
    get_tag_by_tag_id(tag.oid, refresh=1)


def create_tag(**kwargs):
    tag = Tag()
    for attr in tag.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            tag.__updateattr__(attr, value)
    try:
        tag.save()
    except NotUniqueError:
        raise ExistException("Tag")
    return tag


@memorize
def get_tag_by_tag_id(tag_id):
    try:
        _id = ObjectId(tag_id)
        return Tag.objects.get(id=_id)
    except Tag.DoesNotExist:
        raise NotExistException("Tag")


def get_tag_list():
    return Tag.objects.all()


def update_tag(tag, **kwargs):
    for attr in tag.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            tag.__updateattr__(attr, value)
    tag.updated = datetime.datetime.now()
    try:
        tag.save()
    except NotUniqueError:
        raise ExistException("Tag")
    refresh(tag)
    return tag


def delete_tag(tag):
    tag.delete()
    refresh(tag)
    return None


def to_front(tag):
    d = json.loads(tag.to_json())
    d['id'] = tag.oid
    d.pop('_id')
    return ObjectDict(d)
