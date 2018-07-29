# -*- coding: utf-8 -*-

import datetime
import mongoengine as models

class PasswordLock(models.Document):    
    name = models.StringField(unique=True)    
    key = models.StringField()    
    website = models.StringField()    
    user_id = models.StringField()    
    created = models.DateTimeField()    
    updated = models.DateTimeField()

