# -*- coding: utf-8 -*-
# @File    : Movie.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Movie import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Movie(BaseModelDocument):
    title = fields.StringField(allow_none=True)
    year = fields.StringField(allow_none=True)
    summary = fields.StringField(allow_none=True)


NAME_DICT["Movie"] = Movie
