# -*- coding: utf-8 -*-

import json
import datetime
from bson import ObjectId
from tornado.util import ObjectDict
from mongoengine.errors import *
import settings
from const import undefined
from common.Decorator.mem_cache import memorize
from common.Exceptions.ExistException import ExistException
from common.Exceptions.NotExistException import NotExistException
from common.Exceptions.ValidateException import ValidateException
from models import Artical


def create_artical(**kwargs):
    artical = Artical()
    for attr in artical.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            artical.__updateattr__(attr, value)
    try:
        artical.save()
    except NotUniqueError:
        raise ExistException("Artical")
    return artical


@memorize
def get_artical_by_artical_id(artical_id):
    try:
        _id = ObjectId(artical_id)
        return Artical.objects.get(id=_id)
    except Artical.DoesNotExist:
        raise NotExistException("Artical")


def refresh(artical):
    get_artical_by_artical_id(artical.oid, refresh=1)


def get_artical_list():
    return Artical.objects.all()


def update_artical(artical, **kwargs):
    for attr in artical.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            artical.__updateattr__(attr, value)
    artical.updated = datetime.datetime.now()
    try:
        artical.save()
    except NotUniqueError:
        raise ExistException("Artical")
    refresh(artical)
    return artical


def delete_artical(artical):
    artical.delete()
    refresh(artical)
    return None


def to_front(artical):
    d = json.loads(artical.to_json())
    d['id'] = artical.oid
    d.pop('_id')
    return ObjectDict(d)
