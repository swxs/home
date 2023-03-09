# -*- coding: utf-8 -*-
# @File    : dao/password_lock.py
# @AUTH    : code_creater

import logging
import datetime

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.password_lock import PasswordLock as PasswordLockModel

logger = logging.getLogger("main.apps.password_lock.dao.password_lock")


class PasswordLock(BaseDocument):
    id = fields.PrimaryField()
    created = fields.DateTimeField(
        default_create=datetime.datetime.now,
    )
    updated = fields.DateTimeField(
        default_create=datetime.datetime.now,
        default_update=datetime.datetime.now,
    )
    user_id = fields.ObjectIdField()
    name = fields.StringField()
    key = fields.StringField()
    website = fields.StringField()
    used = fields.IntField(
        default_create=0,
    )
    ttype = fields.IntField(
        enums=consts.PASSWORD_LOCK_TTYPE_LIST,
        default_create=consts.PASSWORD_LOCK_TTYPE_COMMON,
    )
    custom = fields.DictField()

    class Meta:
        model = PasswordLockModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)
