# -*- coding: utf-8 -*-

import datetime
import mongoengine as models

class Tag(models.Document):    
    name = models.StringField(unique=True)    
    color = models.StringField()    
    length = models.IntField(default=0)    
    created = models.DateTimeField(default=datetime.datetime.now)    
    updated = models.DateTimeField(default=datetime.datetime.now)

