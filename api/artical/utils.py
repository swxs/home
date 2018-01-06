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

def refresh(artical):
    get_artical_by_artical_id(artical.oid, refresh=1)


@memorize
def get_artical_by_artical_id(artical_id):
    try:
        _id = ObjectId(artical_id)
        return models.Artical.objects.get(id=_id)
    except models.Artical.DoesNotExist:
        raise NotExistException("Artical")


@memorize
def has_artical_by_artical_id(artical_id):
    try:
        if get_artical_by_artical_id(artical_id):
            return True
        else:
            return False
    except NotExistException:
        return False


def get_artical_list():
    return models.Artical.objects.filter()


def create(**kwargs):
    artical = models.Artical()
    for attr in artical.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            artical.__setattr__(attr, value)
    try:
        artical.save()
    except NotUniqueError:
        raise ExistException("Artical")
    return artical


def update(artical, **kwargs):
    for attr in artical.__attrs__:
        value = kwargs.get(attr, undefined)
        if value != undefined:
            artical.__setattr__(attr, value)
    artical.updated = datetime.datetime.now()
    try:
        artical.save()
    except NotUniqueError:
        raise ExistException("Artical")
    refresh(artical)
    return artical


def delete(artical):
    artical.delete()
    refresh(artical)
    return None


def to_front(artical):
    if artical:
        return artical.to_dict()
