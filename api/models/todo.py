# -*- coding: utf-8 -*-

import datetime
import mongoengine as models
from api.consts.todo import *


class Todo(models.Document):
    title = models.StringField()
    summary = models.StringField()
    status = models.IntField(choices=STATUS_TYPES)
    species = models.IntField()
    priority = models.IntField(choices=PRIORITY_TYPES)
    created = models.DateTimeField()
    updated = models.DateTimeField()
