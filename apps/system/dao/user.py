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
