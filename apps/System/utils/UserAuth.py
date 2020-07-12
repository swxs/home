# -*- coding: utf-8 -*-
# @File    : UserAuth.py
# @AUTH    : model_creater

from ..models import UserAuth as UserAuthModel
from ..dao import UserAuth as BaseUserAuth
from marshmallow import Schema, fields

UserAuthSchema = UserAuthModel.schema.as_marshmallow_schema()

user_auth_schema = UserAuthSchema()

class UserAuth(BaseUserAuth):
    def __init__(self, **kwargs):
        super(UserAuth, self).__init__(**kwargs)
