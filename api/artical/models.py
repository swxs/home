# -*- coding: utf-8 -*-

import datetime
import mongoengine as models
from enums import Enums
import utils


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

    __attrs__ = ['title', 'author', 'source', 'summary', 'content', 'tag_id_list', 'comment_id_list']

    def __updateattr__(self, name, value):
        super(Artical, self).__setattr__(name, value)

    def __unicode__(self):
        try:
            return self.title
        except AttributeError:
            return self.oid

    @property
    def oid(self):
        return str(self.id)
