# -*- coding: utf-8 -*-
# @File    : UserAuth.py
# @AUTH    : model_creater

import uuid

from marshmallow import Schema, fields

# 本模块方法
from ..dao import UserAuth as BaseUserAuth
from .User import User
from ..models import UserAuth as UserAuthModel

UserAuthSchema = UserAuthModel.schema.as_marshmallow_schema()

user_auth_schema = UserAuthSchema()


class UserAuth(BaseUserAuth):
    def __init__(self, **kwargs):
        super(UserAuth, self).__init__(**kwargs)

    @classmethod
    async def create(cls, creates):
        if 'user_id' not in creates:
            user = await User.create(dict(username=f"user_{str(uuid.uuid4())}"))
            creates['user_id'] = user.id

        return await super(UserAuth, cls).create(creates)
