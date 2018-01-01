# -*- coding: utf-8 -*-

from bson import ObjectId
import models
from api.tag.utils import utils
from common.Decorator.mem_cache import memorize
from const import undefined


class creater():
    def __init__(self):
        pass

    @classmethod
    @memorize
    def get_tag_by_tag_id(tag_id):
        try:
            _id = ObjectId(tag_id)
            return utils(models.Tag.objects.get(id=_id))
        except models.Tag.DoesNotExist:
            return None

    @classmethod
    def get_tag_list(tag_id):
        return utils(models.Tag.objects.filter())

    @memorize
    @classmethod
    def has_tag_by_tag_id(tag_id):
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
