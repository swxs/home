# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Movie.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Movie import Movie
from common.Utils.log_utils import getLogger

log = getLogger("views/Movie")


class MovieHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, movie_id=None):
        if movie_id:
            movie = Movie.select(id=movie_id)
            return Movie.to_front()
        else:
            movie_list = Movie.filter()
            return [movie.to_front() for movie in movie_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        movie = Movie.create(params)
        return movie.to_front()

    @BaseHandler.ajax_base()
    def put(self, movie_id):
        params = self.get_all_arguments()
        movie = Movie.select(id=movie_id)
        movie = movie.update(params)
        return movie.to_front()

    @BaseHandler.ajax_base()
    def patch(self, movie_id):
        params = self.get_all_arguments()
        movie = Movie.select(id=movie_id)
        movie = movie.update(params)
        return movie.to_front()

    @BaseHandler.ajax_base()
    def delete(self, movie_id):
        movie = Movie.select(id=movie_id)
        movie.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
