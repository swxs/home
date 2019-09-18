# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.User import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class User(BaseModelDocument):
    username = fields.StringField(allow_none=True, helper_text='用户名')
    nickname = fields.StringField(allow_none=True, helper_text='昵称')
    password = fields.StringField(allow_none=True, helper_text='密码')
    salt = fields.StringField(allow_none=True, helper_text='密码盐值')
    avatar = fields.StringField(allow_none=True, helper_text='头像')
    email = fields.StringField(allow_none=True, helper_text='邮箱')
    mobile = fields.StringField(allow_none=True, helper_text='手机号')
    description = fields.StringField(allow_none=True, helper_text='描述')

    class Meta:
        indexes = [
            {
                'key': ['username'],
                'unique': True,
            },
            {
                'key': ['mobile'],
            },
        ]
        pass


NAME_DICT["User"] = User
