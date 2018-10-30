# -*- coding: utf-8 -*-

import datetime
import models_fields
from models_manager.BaseDocument import BaseDocument


class Tag(BaseDocument):
    name = models_fields.StringField()
    color = models_fields.StringField()
    length = models_fields.IntField()
    created = models_fields.DateTimeField()
    updated = models_fields.DateTimeField(pre_update=datetime.datetime.now)

    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
