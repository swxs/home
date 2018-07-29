# -*- coding: utf-8 -*-

import datetime
from BaseDocument import BaseDocument
import models_fields


class Artical(BaseDocument):
    title = models_fields.StringField()
    author = models_fields.StringField()
    source = models_fields.StringField()
    summary = models_fields.StringField()
    content = models_fields.StringField()
    tag_id_list = models_fields.ListField()
    comment_id_list = models_fields.ListField()
    created = models_fields.DateTimeField(default=datetime.datetime.now)
    updated = models_fields.DateTimeField(default=datetime.datetime.now)

    def __init__(self, **kwargs):
        super(Artical, self).__init__(**kwargs)
