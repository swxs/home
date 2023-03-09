# -*- coding: utf-8 -*-
# @File    : dao/user.py
# @AUTH    : code_creater

import logging
import datetime

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.user import User as UserModel

logger = logging.getLogger("main.apps.system.dao.user")


class User(BaseDocument):
    id = fields.PrimaryField()
    created = fields.DateTimeField(
        default_create=datetime.datetime.now,
    )
    updated = fields.DateTimeField(
        default_create=datetime.datetime.now,
        default_update=datetime.datetime.now,
    )
    username = fields.StringField()
    description = fields.StringField()
    avatar = fields.ObjectIdField()

    class Meta:
        model = UserModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
