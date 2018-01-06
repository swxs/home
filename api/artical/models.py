# -*- coding: utf-8 -*-'

import datetime
import mongoengine as models
from api.basedoc import BaseDoc
import enums as enums


class Artical(models.Document, BaseDoc):    
    title = models.StringField()    
    author = models.StringField()    
    source = models.StringField()    
    content = models.StringField()    
    tag_id_list = models.ListField()    
    comment_id_list = models.ListField()    
    summary = models.StringField()    
    created = models.DateTimeField(default=datetime.datetime.now)    
    updated = models.DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': ['title']
    }

    __attrs__ = ['title', 'author', 'source', 'content', 'tag_id_list', 'comment_id_list', 'summary']
