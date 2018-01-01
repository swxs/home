# -*- coding: utf-8 -*-

from bson import ObjectId
import models as models
from common.Decorator.single_or_multeple import single_or_muliteple
from const import undefined
from common.Decorator.mem_cache import memorize
from common.Exceptions.CommonException import CommonException
from common.Exceptions.ExistException import ExistException
from common.Exceptions.NotExistException import NotExistException

class utils():
    def __init__(self, object):
        self.object = object

    @single_or_muliteple
    def update(self, name=undefined, ttype=undefined):
        ''''''
        try:
            if name != undefined:
                self.object.name = name
            if ttype != undefined:
                self.object.ttype = ttype
            self.object.save()
            self.object = self.object.refresh()
            return self.object
        except:
            return self.object

    @single_or_muliteple
    def delete(self):
        ''''''
        try:
            self.object.delete()
            self.object.refresh()
            return True
        except:
            return False

    @single_or_muliteple
    def to_front(self):
        ''''''
        return self.object.to_dict()
