# -*- coding: utf-8 -*-

import datetime
import mongoengine as models
from common.Helpers.Helper_encryption import Encryption
import api.password_lock.enums as enums

class PasswordLock(models.Document):    
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
    def password(self):
        return Encryption.get_password(self.key)
