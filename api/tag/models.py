# -*- coding: utf-8 -*-'

import datetime
import mongoengine as models
from api.basedoc import BaseDoc
import enums as enums

class Tag(models.Document, BaseDoc):
    name = models.StringField(max_length=50)
    ttype = models.IntField(required=True, choices=enums.TAG_TTYPE_LIST)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

    __attrs__ = ["name", "ttype"]
