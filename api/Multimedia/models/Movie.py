# -*- coding: utf-8 -*-
# @File    : Movie.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.Movie import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Movie(BaseModelDocument):
    title = model.StringField()
    year = model.StringField()
    summary = model.StringField()


NAME_DICT["Movie"] = Movie
