# -*- coding: utf-8 -*-

import datetime
import mongoengine as models
from enums import Enums
from utils import Utils


class Tag(models.Document, Utils):
    name = models.StringField(unique=True)
    color = models.StringField()
    length = models.IntField(default=0)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)

    __attrs__ = ['name', 'color', 'length']

    def __setattr__(self, name, value):
        super(Tag, self).__setattr__(name, value)

    def __unicode__(self):
        try:
            return self.oid
        except AttributeError:
            return self.oid

    @property
    def oid(self):
        return str(self.id)

    @property
    def creater(self):
        from creater import Creater
        return Creater()
