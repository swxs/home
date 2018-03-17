# -*- coding: utf-8 -*-

import datetime
import mongoengine as models
import api.user.enums as enums

class User(models.Document):    
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
    
    def __updateattr__(self, name, value):
        super(User, self).__setattr__(name, value)

    def __unicode__(self):
        try:
            return self.username
        except AttributeError:
            return self.oid

    @property
    def oid(self):
        return str(self.id)
