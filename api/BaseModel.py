# -*- coding: utf-8 -*-
# @File    : BaseModel.py.py
# @AUTH    : swxs
# @Time    : 2019/4/3 10:11

import datetime
import mongoengine as model


class BaseModelDocument(model.Document):
    created = model.DateTimeField(default=datetime.datetime.now)
    updated = model.DateTimeField(default=datetime.datetime.now)

    meta = {
        'abstract': True,
        'ordering': ['-created'],
        'indexes': [
            {
                'fields': ['created'],
            },
            {
                'fields': ['updated'],
            },
        ]
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
