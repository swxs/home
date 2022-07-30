# -*- coding: utf-8 -*-
# @File    : dao/user_auth.py
# @AUTH    : code_creater

import logging
import datetime

import bson

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.user_auth import UserAuth as UserAuthModel

logger = logging.getLogger("main.apps.system.dao.user_auth")


class UserAuth(BaseDocument):
    user_id = fields.ObjectIdField(
        allow_none=True,
    )
    ttype = fields.IntField(
        allow_none=True,
        enums=consts.USER_AUTH_TTYPE_LIST,
    )
    identifier = fields.StringField(
        allow_none=True,
    )
    credential = fields.StringField(
        allow_none=True,
    )
    ifverified = fields.IntField(
        allow_none=True,
        enums=consts.USER_AUTH_IFVERIFIED_LIST,
        default=consts.USER_AUTH_IFVERIFIED_FALSE,
    )

    class Meta:
        model = UserAuthModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(UserAuth, self).__init__(**kwargs)
