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
    created = fields.DateTimeField(
        requirement=False,
        default=datetime.datetime.now,
    )
    updated = fields.DateTimeField(
        requirement=False,
        default=datetime.datetime.now,
    )
    user_id = fields.ObjectIdField(
        requirement=False,
    )
    ttype = fields.IntField(
        requirement=False,
        enums=consts.USER_AUTH_TTYPE_LIST,
    )
    identifier = fields.StringField(
        requirement=False,
    )
    credential = fields.StringField(
        requirement=False,
    )
    ifverified = fields.IntField(
        requirement=False,
        enums=consts.USER_AUTH_IFVERIFIED_LIST,
        default=consts.USER_AUTH_IFVERIFIED_FALSE,
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
