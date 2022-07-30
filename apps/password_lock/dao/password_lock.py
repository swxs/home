# -*- coding: utf-8 -*-
# @File    : dao/password_lock.py
# @AUTH    : code_creater

import logging
import datetime

import bson

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.password_lock import PasswordLock as PasswordLockModel

logger = logging.getLogger("main.apps.password_lock.dao.password_lock")


class PasswordLock(BaseDocument):
    name = fields.StringField(
        allow_none=True,
    )
    key = fields.StringField(
        allow_none=True,
    )
    website = fields.StringField(
        allow_none=True,
    )
    user_id = fields.ObjectIdField(
        allow_none=True,
    )
    used = fields.IntField(
        allow_none=True,
        default=0,
    )
    ttype = fields.IntField(
        allow_none=True,
        enums=consts.PASSWORD_LOCK_TTYPE_LIST,
        default=consts.PASSWORD_LOCK_TTYPE_COMMON,
    )
    custom = fields.DictField(
        allow_none=True,
    )

    class Meta:
        model = PasswordLockModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)
