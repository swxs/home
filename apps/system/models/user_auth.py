# -*- coding: utf-8 -*-
# @FILE    : models/user_auth.py
# @AUTH    : code_creater

import datetime

import bson
from umongo import Document, fields

import core

# 本模块方法
from .. import consts


@core.mongodb_instance.register
class UserAuth(Document):
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
