# -*- coding: utf-8 -*-
# @File    : base_server.py
# @AUTH    : model_creater

import os
import json
import thriftpy2
from thriftpy2.rpc import make_server
from rpc.utils import render_thrift
from api.Multimedia.utils.Multimedia import Multimedia


rpc_dir = os.path.abspath(os.path.dirname(__file__))
multimedia_thrift = thriftpy2.load(rpc_dir + "/protocols/main.thrift", module_name="multimedia_thrift")

class BaseDispatcher(object):
    @render_thrift(multimedia_thrift.CreateResult)
    def create_multimedia_artical(self, **kwargs):
        result = multimedia_thrift.CreateResult
        artical = Artical.create(**kwargs)
        result.id = artical.id
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.UpdateResult)
    def update_multimedia_artical(self, artical_id, **kwargs):
        result = multimedia_thrift.UpdateResult()
        artical = Artical.select(id=artical_id)
        artical = artical.update(**kwargs)
        result.id = artical.id
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.DeleteResult)
    def delete_multimedia_artical(self, artical_id):
        result = multimedia_thrift.DeleteResult()
        artical = Artical.select(id=artical_id)
        artical.delete()
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.ArticalResult)
    def select_multimedia_artical(self, artical_id):
        result = artical_thrift.ArticalResult()
        artical = Artical.select(id=artical_id)
        result_object = multimedia_thrift.artical
        result_object.id = str(artical.id)
        result_object.title = artical.title
        result_object.author = artical.author
        result_object.year = artical.year
        result_object.source = artical.source
        result_object.summary = artical.summary
        result_object.content = artical.content
        result_object.ttype_id_list = artical.ttype_id_list
        result_object.tag_id_list = artical.tag_id_list
        result_object.comment_id_list = artical.comment_id_list
        result.artical = result_object
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.ArticalSearchResult)
    def list_multimedia_artical(self):
        result = multimedia_thrift.ArticalSearchResult()
        artical_list = Artical.filter()
        result_object_list = []
        for artical in artical_list:
            result_object = multimedia_thrift.artical
            result_object.id = str(artical.id)
            result_object.title = artical.title
            result_object.author = artical.author
            result_object.year = artical.year
            result_object.source = artical.source
            result_object.summary = artical.summary
            result_object.content = artical.content
            result_object.ttype_id_list = artical.ttype_id_list
            result_object.tag_id_list = artical.tag_id_list
            result_object.comment_id_list = artical.comment_id_list
            result_object_list.append(result_object)
        result.code = 0
        result.artical_list = result_object_list
        return result

    @render_thrift(multimedia_thrift.CreateResult)
    def create_multimedia_movie(self, **kwargs):
        result = multimedia_thrift.CreateResult
        movie = Movie.create(**kwargs)
        result.id = movie.id
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.UpdateResult)
    def update_multimedia_movie(self, movie_id, **kwargs):
        result = multimedia_thrift.UpdateResult()
        movie = Movie.select(id=movie_id)
        movie = movie.update(**kwargs)
        result.id = movie.id
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.DeleteResult)
    def delete_multimedia_movie(self, movie_id):
        result = multimedia_thrift.DeleteResult()
        movie = Movie.select(id=movie_id)
        movie.delete()
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.MovieResult)
    def select_multimedia_movie(self, movie_id):
        result = movie_thrift.MovieResult()
        movie = Movie.select(id=movie_id)
        result_object = multimedia_thrift.movie
        result_object.id = str(movie.id)
        result_object.title = movie.title
        result_object.year = movie.year
        result_object.summary = movie.summary
        result.movie = result_object
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.MovieSearchResult)
    def list_multimedia_movie(self):
        result = multimedia_thrift.MovieSearchResult()
        movie_list = Movie.filter()
        result_object_list = []
        for movie in movie_list:
            result_object = multimedia_thrift.movie
            result_object.id = str(movie.id)
            result_object.title = movie.title
            result_object.year = movie.year
            result_object.summary = movie.summary
            result_object_list.append(result_object)
        result.code = 0
        result.movie_list = result_object_list
        return result

    @render_thrift(multimedia_thrift.CreateResult)
    def create_multimedia_tag(self, **kwargs):
        result = multimedia_thrift.CreateResult
        tag = Tag.create(**kwargs)
        result.id = tag.id
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.UpdateResult)
    def update_multimedia_tag(self, tag_id, **kwargs):
        result = multimedia_thrift.UpdateResult()
        tag = Tag.select(id=tag_id)
        tag = tag.update(**kwargs)
        result.id = tag.id
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.DeleteResult)
    def delete_multimedia_tag(self, tag_id):
        result = multimedia_thrift.DeleteResult()
        tag = Tag.select(id=tag_id)
        tag.delete()
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.TagResult)
    def select_multimedia_tag(self, tag_id):
        result = tag_thrift.TagResult()
        tag = Tag.select(id=tag_id)
        result_object = multimedia_thrift.tag
        result_object.id = str(tag.id)
        result_object.name = tag.name
        result_object.color = tag.color
        result.tag = result_object
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.TagSearchResult)
    def list_multimedia_tag(self):
        result = multimedia_thrift.TagSearchResult()
        tag_list = Tag.filter()
        result_object_list = []
        for tag in tag_list:
            result_object = multimedia_thrift.tag
            result_object.id = str(tag.id)
            result_object.name = tag.name
            result_object.color = tag.color
            result_object_list.append(result_object)
        result.code = 0
        result.tag_list = result_object_list
        return result

    @render_thrift(multimedia_thrift.CreateResult)
    def create_multimedia_ttype(self, **kwargs):
        result = multimedia_thrift.CreateResult
        ttype = Ttype.create(**kwargs)
        result.id = ttype.id
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.UpdateResult)
    def update_multimedia_ttype(self, ttype_id, **kwargs):
        result = multimedia_thrift.UpdateResult()
        ttype = Ttype.select(id=ttype_id)
        ttype = ttype.update(**kwargs)
        result.id = ttype.id
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.DeleteResult)
    def delete_multimedia_ttype(self, ttype_id):
        result = multimedia_thrift.DeleteResult()
        ttype = Ttype.select(id=ttype_id)
        ttype.delete()
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.TtypeResult)
    def select_multimedia_ttype(self, ttype_id):
        result = ttype_thrift.TtypeResult()
        ttype = Ttype.select(id=ttype_id)
        result_object = multimedia_thrift.ttype
        result_object.id = str(ttype.id)
        result_object.name = ttype.name
        result.ttype = result_object
        result.code = 0
        return result

    @render_thrift(multimedia_thrift.TtypeSearchResult)
    def list_multimedia_ttype(self):
        result = multimedia_thrift.TtypeSearchResult()
        ttype_list = Ttype.filter()
        result_object_list = []
        for ttype in ttype_list:
            result_object = multimedia_thrift.ttype
            result_object.id = str(ttype.id)
            result_object.name = ttype.name
            result_object_list.append(result_object)
        result.code = 0
        result.ttype_list = result_object_list
        return result



if __name__ == '__main__':
    from ..client_pool import get_rpc_server_host, get_rpc_server_port

    server = make_server(
        multimedia_thrift.MultimediaService,
        BaseDispatcher(),
        get_rpc_server_host('Multimedia'),
        get_rpc_server_port('Multimedia'),
        client_timeout=None
    )
    server.serve()