# -*- coding: utf-8 -*-'

import datetime
import mongoengine as models
from api.basedoc import BaseDoc
import enums as enums


class Tag(models.Document, BaseDoc):    
    name = models.StringField(unique=True)    
    color = models.StringField()    
    length = models.IntField(default=0)    
    created = models.DateTimeField(default=datetime.datetime.now)    
    updated = models.DateTimeField(default=datetime.datetime.now)

    __attrs__ = ['name', 'color', 'length']
