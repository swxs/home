# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model_creater

import bson
import datetime
import logging

from dao import BaseDocument, fields
from ..consts import common_enum
from ..models.password_lock import PasswordLock as PasswordLockModel

logger = logging.getLogger("main.password_lock.dao")


class PasswordLock(BaseDocument):
    name = fields.StringField()
    key = fields.StringField()
    website = fields.StringField()
    user_id = fields.ObjectIdField()
    used = fields.IntField(default=0)
    ttype = fields.IntField(enums=common_enum.PASSWORD_LOCK_TTYPE_LIST, default=common_enum.PASSWORD_LOCK_TTYPE_COMMON)
    custom = fields.DictField()
    created = fields.DateTimeField(create=False)
    updated = fields.DateTimeField(create=False, pre_update=datetime.datetime.now)

    class Meta:
        model = PasswordLockModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)
