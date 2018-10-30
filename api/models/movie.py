# -*- coding: utf-8 -*-

import datetime
import mongoengine as models
from api.consts.movie import *

class Movie(models.Document):
    name = models.StringField()
    nickname = models.StringField()
    year = models.StringField()
    type_id = models.StringField(max_length=24)
    tag_id_list = models.ListField()
    description = models.StringField()
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

