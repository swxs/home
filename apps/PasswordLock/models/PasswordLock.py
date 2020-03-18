# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.PasswordLock import *
from ...BaseModel import BaseModelDocument
from settings import instance


@instance.register
class PasswordLock(BaseModelDocument):
    name = fields.StringField(allow_none=True)
    key = fields.StringField(allow_none=True)
    website = fields.StringField(allow_none=True)
    user_id = fields.ObjectIdField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['user_id, name'],
            },
        ]
        pass
