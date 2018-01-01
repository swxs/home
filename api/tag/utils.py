# -*- coding: utf-8 -*-

from api.baseUtils import utils as base_utils
from const import undefined


class utils(base_utils):
    def __init__(self, object):
        self.object = object

    @base_utils.single_or_multiple
    def update(self, name=undefined, ttype=undefined, object=None):
        ''''''
        try:
            if name != undefined:
                object.name = name
            if ttype != undefined:
                object.ttype = ttype
            object.save()
            return True
        except:
            return False

    @base_utils.single_or_multiple
    def delete(self, object=None):
        ''''''
        try:
            object.delete()
            return True
        except:
            return False

    @base_utils.single_or_multiple
    def to_front(self, object=None):
        ''''''
        return object.to_dict()
