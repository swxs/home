# -*- coding: utf-8 -*-
        
import json
import datetime
import enum as enum
import mongoengine as models
from basedoc import BaseDoc as BaseDoc


class Tag(models.Document, BaseDoc):    
    name = models.StringField(required=False, max_length=50)
    ttype = models.IntField(required=True, choices=enum.TAG_TTYPE_LIST)

    def refresh(self):
        from api.tag.creater import creater
        creater.get_tag_by_tag_id(str(self.id), refresh=1)

