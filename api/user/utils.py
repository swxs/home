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
    def update_user(self, **kwargs):
        for attr in self.__attrs__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                self.__updateattr__(attr, value)
        self.updated = datetime.datetime.now()
        try:
            self.save()
        except NotUniqueError:
            raise ExistException("User")
        self.creater.refresh(self)
        return self

    def delete_user(self):
        self.delete()
        self.creater.refresh(self)
        return None

    def to_front(self):
        return self.to_dict()

    def get_real_password(self, password):
        try:
            if password is None:
                return None
            else:
                return md5(settings.SECRET_KEY + password).hexdigest()
        except:
            raise ValidateException("password")
