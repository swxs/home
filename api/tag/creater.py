# -*- coding: utf-8 -*-

from hashlib import md5
from bson import ObjectId
from mongoengine.errors import *
import settings
from const import undefined
from models import Tag
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
    def create_tag(cls, **kwargs):
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

    @classmethod
    def refresh(cls, tag):
        cls.get_tag_by_tag_id(tag.oid, refresh=1)

    @classmethod
    @memorize
    def get_tag_by_tag_id(cls, tag_id):
        try:
            _id = ObjectId(tag_id)
            return Tag.objects.get(id=_id)
        except Tag.DoesNotExist:
            raise NotExistException("Tag")

    @classmethod
    @memorize
    def has_tag_by_tag_id(cls, tag_id):
        try:
            if Creater.get_tag_by_tag_id(tag_id):
                return True
            else:
                return False
        except NotExistException:
            return False

    @classmethod
    def get_tag_list(cls):
        return Collections(Tag.objects.all())
