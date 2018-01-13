# -*- coding: utf-8 -*-

import datetime
import mongoengine as models
from enums import Enums
from utils import Utils


class User(models.Document, Utils):
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

    def __unicode__(self):
        try:
            return self.username
        except AttributeError:
            return self.oid

    @property
    def oid(self):
        return str(self.id)

    @property
    def creater(self):
        from creater import Creater
        return Creater()
