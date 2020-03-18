# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.User import *
from ...BaseModel import BaseModelDocument
from settings import instance


@instance.register
class User(BaseModelDocument):
    org_id = fields.ObjectIdField(allow_none=True)
    salt = fields.StringField(allow_none=True)
    username = fields.StringField(allow_none=True)
    nickname = fields.StringField(allow_none=True)
    password = fields.StringField(allow_none=True)
    phone = fields.StringField(allow_none=True)
    email = fields.StringField(allow_none=True)
    avatar = fields.StringField(allow_none=True)
    description = fields.StringField(allow_none=True)

    class Meta:
        pass
