# -*- coding: utf-8 -*-
# @FILE    : models.py
# @AUTH    : model_creater

import bson
import datetime
from umongo import Instance, Document, fields
from dao.manager.manager_umongo_motor import NAME_DICT
from ..BaseModel import BaseModelDocument
from . import consts
from settings import MONGO_INSTANCE


@MONGO_INSTANCE.register
class PasswordLock(Document):
    name = fields.StringField(allow_none=True)
    key = fields.StringField(allow_none=True)
    website = fields.StringField(allow_none=True)
    user_id = fields.ObjectIdField(allow_none=True)
    used = fields.IntField(allow_none=True, default=0)
    ttype = fields.IntField(
        allow_none=True, enums=consts.PASSWORD_LOCK_TTYPE_LIST, default=consts.PASSWORD_LOCK_TTYPE_COMMON
    )
    custom = fields.DictField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['user_id, name'],
            },
        ]
        pass


NAME_DICT["PasswordLock"] = PasswordLock
