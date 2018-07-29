# -*- coding: utf-8 -*-
# @File    : utils.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:55

import datetime
from BaseDocument import BaseDocument
import models_fields


class User(BaseDocument):
    username = models_fields.StringField()
    nickname = models_fields.StringField()
    password = models_fields.StringField()
    userinfo_id = models_fields.StringField()
    created = models_fields.DateTimeField()
    updated = models_fields.DateTimeField(update=datetime.datetime.now)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
