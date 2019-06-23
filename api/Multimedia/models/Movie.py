# -*- coding: utf-8 -*-
# @File    : Movie.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Movie import *
from ...BaseModel import BaseModelDocument
from document_utils import NAME_DICT


class Movie(BaseModelDocument):
    title = model.StringField()
    year = model.StringField()
    summary = model.StringField()


NAME_DICT["Movie"] = Movie
