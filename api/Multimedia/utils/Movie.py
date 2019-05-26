# -*- coding: utf-8 -*-
# @File    : Movie.py
# @AUTH    : model_creater

from ..commons.Movie import Movie as BaseMovie


class Movie(BaseMovie):
    def __init__(self, **kwargs):
        super(Movie, self).__init__(**kwargs)
