# -*- coding: utf-8 -*-
# @File    : Artical.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Artical import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Artical(BaseModelDocument):
    title = fields.StringField(allow_none=True)
    author = fields.StringField(allow_none=True)
    year = fields.StringField(allow_none=True)
    source = fields.StringField(allow_none=True)
    summary = fields.StringField(allow_none=True)
    content = fields.StringField(allow_none=True)
    ttype_id_list = fields.StringField(allow_none=True)
    tag_id_list = fields.StringField(allow_none=True)
    comment_id_list = fields.StringField(allow_none=True)


NAME_DICT["Artical"] = Artical
