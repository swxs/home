# -*- coding: utf-8 -*-
        
import datetime
import models_fields
from api.consts.movie import *
from models_manager.BaseDocument import BaseDocument


class Movie(BaseDocument):
    name = models_fields.StringField()
    nickname = models_fields.StringField()
    year = models_fields.StringField()
    type_id = models_fields.StringField(max_length=24)
    tag_id_list = models_fields.ListField()
    description = models_fields.StringField()
    created = models_fields.DateTimeField(default=datetime.datetime.now)
    updated = models_fields.DateTimeField(default=datetime.datetime.now, pre_update=datetime.datetime.now)

    def __init__(self, **kwargs):
        super(Movie, self).__init__(**kwargs)
