# -*- coding: utf-8 -*-

import datetime
from hashlib import md5
from mongoengine.errors import *
import settings
from const import undefined
from api.base_utils import BaseUtils
from common.Exceptions.ExistException import ExistException
from common.Exceptions.NotExistException import NotExistException
from common.Exceptions.ValidateException import ValidateException

class Utils(BaseUtils):
    def update_tag(self, **kwargs):
        for attr in self.__attrs__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                self.__updateattr__(attr, value)
        self.updated = datetime.datetime.now()
        try:
            self.save()
        except NotUniqueError:
            raise ExistException("Tag")
        self.creater.refresh(self)
        return self

    def delete_tag(self):
        self.delete()
        self.creater.refresh(self)
        return None

    def to_front(self):
        return self.to_dict()
