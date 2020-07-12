# -*- coding: utf-8 -*-
# @FILE    : models.py
# @AUTH    : model_creater

import datetime
import uuid
from umongo import Instance, Document, fields
from dao.manager.manager_umongo_motor import NAME_DICT
from ..BaseModel import BaseModelDocument
from . import consts
from settings import instance


@instance.register
class User(BaseModelDocument):
    username = fields.StringField(allow_none=True)
    description = fields.StringField(allow_none=True)
    avatar = fields.ObjectIdField(allow_none=True)
    salt = fields.StringField(allow_none=True, default=str(uuid.uuid4()))


@instance.register
class UserAuth(BaseModelDocument):
    user_id = fields.ObjectIdField(allow_none=True)
    ttype = fields.IntField(allow_none=True, enums=consts.USER_AUTH_TTYPE_LIST)
    identifier = fields.StringField(allow_none=True)
    credential = fields.StringField(allow_none=True)
    ifverified = fields.IntField(allow_none=True, enums=consts.USER_AUTH_IFVERIFIED_LIST, default=consts.USER_AUTH_IFVERIFIED_FALSE)

    class Meta:
        indexes = [
            {
                'key': ['user_id'],
            },
            {
                'key': ['ttype, identifier'],
            },
        ]
        pass


NAME_DICT["User"] = User
NAME_DICT["UserAuth"] = UserAuth
