# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.PasswordLock import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class PasswordLock(BaseModelDocument):
    name = model.StringField()
    key = model.StringField()
    website = model.StringField()
    user_id = model.ObjectIdField()


NAME_DICT["PasswordLock"] = PasswordLock
