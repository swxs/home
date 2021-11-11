# -*- coding: utf-8 -*-
# @FILE    : models.py
# @AUTH    : model_creater

import bson
import datetime
from umongo import Instance, Document, fields
import core
from dao.managers.manager_umongo_motor import NAME_DICT
from . import consts


@instance.register
class User(BaseModelDocument):
    username = fields.StringField(allow_none=True)
    description = fields.StringField(allow_none=True)
    avatar = fields.ObjectIdField(allow_none=True)


@instance.register
class UserAuth(BaseModelDocument):
    user_id = fields.ObjectIdField(allow_none=True)
    ttype = fields.IntField(allow_none=True, enums=consts.USER_AUTH_TTYPE_LIST)
    identifier = fields.StringField(allow_none=True)
    credential = fields.StringField(allow_none=True)
    ifverified = fields.IntField(
        allow_none=True, enums=consts.USER_AUTH_IFVERIFIED_LIST, default=consts.USER_AUTH_IFVERIFIED_FALSE
    )

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
