# -*- coding: utf-8 -*-
# @FILE    : dao.py
# @AUTH    : model_creater

import bson
import logging
from dao import fields
from ..BaseDAO import BaseDAO
from . import consts

logger = logging.getLogger("main.password_lock.dao")


class PasswordLock(BaseDAO):
    name = fields.StringField()
    key = fields.StringField()
    website = fields.StringField()
    user_id = fields.ObjectIdField()
    used = fields.IntField(default=0)
    ttype = fields.IntField(enums=consts.PASSWORD_LOCK_TTYPE_LIST, default=consts.PASSWORD_LOCK_TTYPE_COMMON)
    custom = fields.DictField()

    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)

    @classmethod
    async def get_password_lock_by_password_lock_id(cls, password_lock_id):
        return await cls.find(dict(id=password_lock_id))
