# -*- coding: utf-8 -*-
# @File    : UserAuth.py
# @AUTH    : model_creater

import uuid
from ..models import UserAuth as UserAuthModel
from ..dao import UserAuth as BaseUserAuth
from marshmallow import Schema, fields
from .User import User

UserAuthSchema = UserAuthModel.schema.as_marshmallow_schema()

user_auth_schema = UserAuthSchema()

class UserAuth(BaseUserAuth):
    def __init__(self, **kwargs):
        super(UserAuth, self).__init__(**kwargs)

    @classmethod
    async def create(cls, **kwargs):
        if 'user_id' not in kwargs:
            user = await User.create(username=f"user_{str(uuid.uuid4())}")
            kwargs['user_id'] = user.id

        return await super(UserAuth, cls).create(**kwargs)
