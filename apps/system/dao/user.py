# -*- coding: utf-8 -*-
# @File    : dao/user.py
# @AUTH    : code_creater

import logging
import datetime

import bson

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.user import User as UserModel

logger = logging.getLogger("main.apps.system.dao.user")


class User(BaseDocument):
    id = fields.ObjectIdField(
        allow_none=False,
        default_create=bson.ObjectId,
    )
    created = fields.DateTimeField(
        allow_none=False,
        default_create=datetime.datetime.now,
    )
    updated = fields.DateTimeField(
        allow_none=False,
        default_create=datetime.datetime.now,
        default_update=datetime.datetime.now,
    )
    username = fields.StringField(
        allow_none=False,
    )
    description = fields.StringField(
        allow_none=True,
    )
    avatar = fields.ObjectIdField(
        allow_none=True,
    )

    class Meta:
        model = UserModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
