# -*- coding: utf-8 -*-

import mongoengine as models

import enum as enum
from api.basedoc import BaseDoc


class Tag(models.Document, BaseDoc):
    name = models.StringField(max_length=50)
    ttype = models.IntField(required=True, choices=enum.TAG_TTYPE_LIST)

    def refresh(self):
        from creater import creater
        creater.get_tag_by_tag_id(str(self.id), refresh=1)
