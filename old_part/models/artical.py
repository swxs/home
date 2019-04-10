# -*- coding: utf-8 -*-

import datetime
import mongoengine as models


class Artical(models.Document):
    title = models.StringField()
    author = models.StringField()
    source = models.StringField()
    summary = models.StringField()
    content = models.StringField()
    tag_id_list = models.ListField()
    comment_id_list = models.ListField()
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': ['title']
    }
