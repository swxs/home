# -*- coding: utf-8 -*-

import datetime
import mongoengine as models
from enums import Enums
from utils import Utils
from common.Helpers.Helper_encryption import Encryption


class PasswordLock(models.Document, Utils):
    name = models.StringField(unique=True)
    key = models.StringField()
    website = models.StringField()
    user_id = models.StringField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    __attrs__ = ['name', 'website', 'user_id']

    def __updateattr__(self, name, value):
        super(PasswordLock, self).__setattr__(name, value)

    def __unicode__(self):
        try:
            return self.name
        except AttributeError:
            return self.oid

    @property
    def oid(self):
        return str(self.id)

    @property
    def creater(self):
        from creater import Creater
        return Creater()

    @property
    def password(self):
        return Encryption.get_password(self.key)
