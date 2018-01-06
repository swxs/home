# -*- coding: utf-8 -*-'

import datetime
import mongoengine as models
from api.basedoc import BaseDoc
import enums as enums


class User(models.Document, BaseDoc):
    username = models.StringField(unique=True)
    nickname = models.StringField()
    password = models.StringField()
    userinfo_id = models.StringField(max_length=24)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': ['username']
    }

    __attrs__ = ['username', 'nickname', 'password', 'userinfo_id']
