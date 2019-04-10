# -*- coding: utf-8 -*-
# @File    : Movie.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.Movie import Movie

log = getLogger("views/Movie")


class MovieHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, movie_id=None):
        if movie_id:
            movie = Movie.select(id=movie_id)
            return movie.to_front()
        else:
            movie_list = Movie.filter()
            return [movie.to_front() for movie in movie_list]

    @BaseHandler.ajax_base()
    def post(self, movie_id=None):
        params = dict()
        params['title'] = self.get_argument('title', None)
        params['year'] = self.get_argument('year', None)
        params['summary'] = self.get_argument('summary', None)
        movie = Movie.create(**params)
        return movie.id

    @BaseHandler.ajax_base()
    def put(self, movie_id=None):
        params = dict()
        params['title'] = self.get_argument('title', None)
        params['year'] = self.get_argument('year', None)
        params['summary'] = self.get_argument('summary', None)
        movie = Movie.select(id=movie_id)
        movie = movie.update(**params)
        return movie.id

    @BaseHandler.ajax_base()
    def patch(self, movie_id=None):
        params = dict()
        params['title'] = self.get_argument('title', undefined)
        params['year'] = self.get_argument('year', undefined)
        params['summary'] = self.get_argument('summary', undefined)
        movie = Movie.select(id=movie_id)
        movie = movie.update(**params)
        return movie.id

    @BaseHandler.ajax_base()
    def delete(self, movie_id=None):
        movie = Movie.select(id=movie_id)
        movie.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
