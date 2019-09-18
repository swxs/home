# -*- coding: utf-8 -*-
# @File    : BaseModel.py.py
# @AUTH    : swxs
# @Time    : 2019/4/3 10:11

import datetime
from settings import instance
from umongo import Instance, Document, fields, ValidationError, set_gettext
from umongo.marshmallow_bonus import SchemaFromUmongo

@instance.register
class BaseModelDocument(Document):
    created = fields.DateTimeField(default=datetime.datetime.now)
    updated = fields.DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True
        allow_inheritance = True

    # meta = {
    #     'abstract': True,
    #     'ordering': ['-created'],
    # }

