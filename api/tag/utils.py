# -*- coding: utf-8 -*-

import datetime
from BaseDocument import BaseDocument
import models_fields


class Tag(BaseDocument):
    name = models_fields.StringField(unique=True)
    color = models_fields.StringField()
    length = models_fields.IntField(default=0)
    created = models_fields.DateTimeField(default=datetime.datetime.now)
    updated = models_fields.DateTimeField(default=datetime.datetime.now)

    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
