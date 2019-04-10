# -*- coding: utf-8 -*-
        
import datetime
import models_fields
from models_manager.BaseDocument import BaseDocument


class Todo(BaseDocument):    
    title = models_fields.StringField()
    summary = models_fields.StringField()
    status = models_fields.IntField()
    species = models_fields.IntField()
    priority = models_fields.IntField()
    created = models_fields.DateTimeField()    
    updated = models_fields.DateTimeField()

    def __init__(self, **kwargs):
        super(Todo, self).__init__(**kwargs)
