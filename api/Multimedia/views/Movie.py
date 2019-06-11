# -*- coding: utf-8 -*-
# @File    : Movie.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Movie import Movie

log = getLogger("views/Movie")


class MovieHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, movie_id=None):
        if movie_id:
            movie = Movie.select(id=movie_id)
            return SuccessData(
                movie.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            movie_list = Movie.search(**search_params).order_by()
            pager = Page(movie_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, movie_id=None):
        if movie_id:
            params = dict()
            params['title'] = self.get_argument('title', undefined)
            params['year'] = self.get_argument('year', undefined)
            params['summary'] = self.get_argument('summary', undefined)
            movie = Movie.select(id=movie_id)
            movie = movie.copy(**params)
            return SuccessData(
                movie.id
            )
        else:
            params = dict()
            params['title'] = self.get_argument('title', None)
            params['year'] = self.get_argument('year', None)
            params['summary'] = self.get_argument('summary', None)
            movie = Movie.create(**params)
            return SuccessData(
                movie.id
            )

    @BaseHandler.ajax_base()
    def put(self, movie_id=None):
        params = dict()
        params['title'] = self.get_argument('title', None)
        params['year'] = self.get_argument('year', None)
        params['summary'] = self.get_argument('summary', None)
        movie = Movie.select(id=movie_id)
        movie = movie.update(**params)
        return SuccessData(
            movie.id
        )

    @BaseHandler.ajax_base()
    def patch(self, movie_id=None):
        params = dict()
        params['title'] = self.get_argument('title', undefined)
        params['year'] = self.get_argument('year', undefined)
        params['summary'] = self.get_argument('summary', undefined)
        movie = Movie.select(id=movie_id)
        movie = movie.update(**params)
        return SuccessData(
            movie.id
        )

    @BaseHandler.ajax_base()
    def delete(self, movie_id=None):
        movie = Movie.select(id=movie_id)
        movie.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
