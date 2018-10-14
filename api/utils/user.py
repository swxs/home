# -*- coding: utf-8 -*-
# @File    : user.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import uuid
import datetime
import models_fields
import settings
from common.Helpers.Helper_encryption import Encryption
from models_manager.BaseDocument import BaseDocument
from common.Utils.validate import RegType


class User(BaseDocument):
    username = models_fields.StringField()
    nickname = models_fields.StringField()
    password = models_fields.StringField()
    key = models_fields.StringField(default=uuid.uuid4)
    userinfo_id = models_fields.StringField()
    created = models_fields.DateTimeField()
    updated = models_fields.DateTimeField(pre_update=datetime.datetime.now)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)



    @classmethod
    def create(cls, **kwargs):
        kwargs["password"] = Encryption.get_md5(kwargs["password"], settings.SALT)
        return super(User, cls).create(**kwargs)