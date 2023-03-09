# -*- coding: utf-8 -*-
# @File    : dao/user_auth.py
# @AUTH    : code_creater

import logging
import datetime

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.user_auth import UserAuth as UserAuthModel

logger = logging.getLogger("main.apps.system.dao.user_auth")


class UserAuth(BaseDocument):
    id = fields.PrimaryField()
    created = fields.DateTimeField(
        default_create=datetime.datetime.now,
    )
    updated = fields.DateTimeField(
        default_create=datetime.datetime.now,
        default_update=datetime.datetime.now,
    )
    user_id = fields.ObjectIdField()
    ttype = fields.IntField(
        enums=consts.USER_AUTH_TTYPE_LIST,
    )
    identifier = fields.StringField()
    credential = fields.StringField()
    ifverified = fields.IntField(
        enums=consts.USER_AUTH_IFVERIFIED_LIST,
        default_create=consts.USER_AUTH_IFVERIFIED_FALSE,
    )

    class Meta:
        model = UserAuthModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(UserAuth, self).__init__(**kwargs)
