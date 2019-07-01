# -*- coding: utf-8 -*-
# @File    : Artical.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Artical import *
from ...BaseModel import BaseModelDocument
from document_utils import NAME_DICT


class Artical(BaseModelDocument):
    title = model.StringField()
    author = model.StringField()
    year = model.StringField()
    source = model.StringField()
    summary = model.StringField()
    content = model.StringField()
    ttype_id_list = model.StringField()
    tag_id_list = model.StringField()
    comment_id_list = model.StringField()


NAME_DICT["Artical"] = Artical
