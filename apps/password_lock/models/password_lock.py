# -*- coding: utf-8 -*-
# @FILE    : models/password_lock.py
# @AUTH    : code_creater

import datetime

import bson
from umongo import Document, fields

import core

# 本模块方法
from .. import consts


@core.mongodb_instance.register
class PasswordLock(Document):
    name = fields.StringField(
        requirement=False,
    )
    key = fields.StringField(
        requirement=False,
    )
    website = fields.StringField(
        requirement=False,
    )
    user_id = fields.ObjectIdField(
        requirement=False,
    )
    used = fields.IntField(
        requirement=False,
        default=0,
    )
    ttype = fields.IntField(
        requirement=False,
        enums=consts.PASSWORD_LOCK_TTYPE_LIST,
        default=consts.PASSWORD_LOCK_TTYPE_COMMON,
    )
    custom = fields.DictField(
        requirement=False,
    )

    class Meta:
        indexes = [
            {
                'key': ['user_id, name'],
            },
        ]
        pass
