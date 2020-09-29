# -*- coding: utf-8 -*-
# @FILE    : dao.py
# @AUTH    : model_creater

import bson
import logging
from dao import fields
from ..BaseDAO import BaseDAO
from . import consts

logger = logging.getLogger("dao")


class User(BaseDAO):
    username = fields.StringField()
    description = fields.StringField()
    avatar = fields.ObjectIdField()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @classmethod
    async def get_user_by_user_id(cls, user_id):
        return await cls.find(dict(id=user_id))


class UserAuth(BaseDAO):
    user_id = fields.ObjectIdField()
    ttype = fields.IntField(enums=consts.USER_AUTH_TTYPE_LIST)
    identifier = fields.StringField()
    credential = fields.StringField()
    ifverified = fields.IntField(enums=consts.USER_AUTH_IFVERIFIED_LIST, default=consts.USER_AUTH_IFVERIFIED_FALSE)

    def __init__(self, **kwargs):
        super(UserAuth, self).__init__(**kwargs)

    @classmethod
    async def get_user_auth_by_user_auth_id(cls, user_auth_id):
        return await cls.find(dict(id=user_auth_id))
