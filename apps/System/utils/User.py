# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model_creater

from ..models import User as UserModel
from ..dao import User as BaseUser
from marshmallow import Schema, fields

UserSchema = UserModel.schema.as_marshmallow_schema()

user_schema = UserSchema()

class User(BaseUser):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
