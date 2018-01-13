# -*- coding: utf-8 -*-

from hashlib import md5
from bson import ObjectId
from mongoengine.errors import *
import settings
from const import undefined
from models import Artical
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
    def create_artical(cls, **kwargs):
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

    @classmethod
    def refresh(cls, artical):
        cls.get_artical_by_artical_id(artical.oid, refresh=1)

    @classmethod
    @memorize
    def get_artical_by_artical_id(cls, artical_id):
        try:
            _id = ObjectId(artical_id)
            return Artical.objects.get(id=_id)
        except Artical.DoesNotExist:
            raise NotExistException("Artical")

    @classmethod
    @memorize
    def has_artical_by_artical_id(cls, artical_id):
        try:
            if Creater.get_artical_by_artical_id(artical_id):
                return True
            else:
                return False
        except NotExistException:
            return False

    @classmethod
    def get_artical_list(cls):
        return Collections(Artical.objects.all())
