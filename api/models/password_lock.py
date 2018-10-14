# -*- coding: utf-8 -*-

import datetime
import mongoengine as models


class PasswordLock(models.Document):
    name = models.StringField()
    key = models.StringField()
    website = models.StringField()
    user_id = models.StringField(max_length=24)
    created = models.DateTimeField()
    updated = models.DateTimeField()
