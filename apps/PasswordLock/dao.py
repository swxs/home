# -*- coding: utf-8 -*-
# @FILE    : dao.py
# @AUTH    : model_creater

import bson
from dao import fields
from ..BaseDAO import BaseDAO
from . import consts
from common.Utils.log_utils import getLogger

log = getLogger("dao")


class PasswordLock(BaseDAO):
    name = fields.StringField()
    key = fields.StringField()
    website = fields.StringField()
    user_id = fields.ObjectIdField()

    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)

    @classmethod
    async def get_password_lock_by_password_lock_id(cls, password_lock_id):
        return await cls.find(dict(id=password_lock_id))
