# -*- coding: utf-8 -*-
# @File    : Movie.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.Movie import Movie as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Movie(BaseUtils):
    title = model.StringField()
    year = model.StringField()
    summary = model.StringField()

    def __init__(self, **kwargs):
        super(Movie, self).__init__(**kwargs)

    @classmethod
    def get_movie_by_movie_id(cls, movie_id):
        return cls.select(id=movie_id)

