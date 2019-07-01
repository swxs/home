# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.User import *
from ...BaseModel import BaseModelDocument
from document_utils import NAME_DICT


class User(BaseModelDocument):
    username = model.StringField(helper_text='用户名')
    nickname = model.StringField(helper_text='昵称')
    password = model.StringField(helper_text='密码')
    salt = model.StringField(helper_text='密码盐值')
    avatar = model.StringField(helper_text='头像')
    email = model.StringField(helper_text='邮箱')
    mobile = model.StringField(helper_text='手机号')
    description = model.StringField(helper_text='描述')

    meta = {
        'indexes': [
            {
                'fields': ['username'],
                'unique ': True,
            },
            {
                'fields': ['mobile'],
            },
        ],
    }


NAME_DICT["User"] = User
