# -*- coding: utf-8 -*-

import models
from bson import ObjectId
from const import undefined
from utils import utils
from common.Decorator.mem_cache import memorize


class creater():
    def __init__(self):
        pass

    @classmethod
    @memorize
    def get_tag_by_tag_id(cls, tag_id):
        try:
            _id = ObjectId(tag_id)
            return utils(models.Tag.objects.get(id=_id))
        except models.Tag.DoesNotExist:
            return None

    @classmethod
    def get_tag_list(cls):
        return utils(models.Tag.objects.filter())

    @classmethod
    @memorize
    def has_tag_by_tag_id(cls, tag_id):
        ''''''
        try:
            if creater.get_tag_by_tag_id(tag_id):
                return True
            else:
                return False
        except models.Tag.DoesNotExist:
            return False

    @classmethod
    def create(cls, name=undefined, ttype=undefined):
        ''''''
        object = models.Tag()
        if name != undefined:
            object.name = name
        if ttype != undefined:
            object.ttype = ttype
        object.save()
        return utils(object)
