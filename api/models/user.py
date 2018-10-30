# -*- coding: utf-8 -*-
# @File    : user.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:53
import re
import uuid
import datetime
import mongoengine as models


class User(models.Document):
    username = models.StringField(unique=True)
    nickname = models.StringField()
    password = models.StringField()
    key = models.StringField(default=lambda: re.sub("-", "", str(uuid.uuid4())))
    userinfo_id = models.StringField(max_length=24)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': ['username']
    }