# -*- coding: utf-8 -*-

from base import BaseHandler
from api.consts.const import undefined
from api.utils.movie import Movie
    
    
class MovieHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def head(self, *args, **kwargs):
        return {"fields": Movie.__fields__, "methods": ["head", "get", "post", "put", "patch", "delete"]}

    @BaseHandler.ajax_base()
    def get(self, movie_id=None):
        if movie_id:
            movie = Movie.select(id=movie_id)
            return movie.to_front()
        else:
            movie_list = Movie.filter()
            return [movie.to_front() for movie in movie_list]
    
    @BaseHandler.ajax_base()
    def post(self):
        name = self.get_argument('name', None)
        nickname = self.get_argument('nickname', None)
        year = self.get_argument('year', None)
        type_id = self.get_argument('type_id', None)
        tag_id_list = self.get_arguments('tag_id_list', None)
        description = self.get_argument('description', None)
        movie = Movie.create(name=name, nickname=nickname, year=year, type_id=type_id, tag_id_list=tag_id_list, description=description)
        return movie.to_front()

    @BaseHandler.ajax_base()
    def put(self, movie_id):
        name = self.get_argument('name', None)
        nickname = self.get_argument('nickname', None)
        year = self.get_argument('year', None)
        type_id = self.get_argument('type_id', None)
        tag_id_list = self.get_arguments('tag_id_list', None)
        description = self.get_argument('description', None)
        movie = Movie.select(id=movie_id)
        movie = movie.update(name=name, nickname=nickname, year=year, type_id=type_id, tag_id_list=tag_id_list, description=description)
        return movie.to_front()

    @BaseHandler.ajax_base()
    def patch(self, movie_id):
        name = self.get_argument('name', undefined)
        nickname = self.get_argument('nickname', undefined)
        year = self.get_argument('year', undefined)
        type_id = self.get_argument('type_id', undefined)
        tag_id_list = self.get_arguments('tag_id_list', undefined)
        description = self.get_argument('description', undefined)
        movie = Movie.select(id=movie_id)
        movie = movie.update(name=name, nickname=nickname, year=year, type_id=type_id, tag_id_list=tag_id_list, description=description)
        return movie.to_front()

    @BaseHandler.ajax_base()
    def delete(self, movie_id):
        movie = Movie.select(id=movie_id)
        movie.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
