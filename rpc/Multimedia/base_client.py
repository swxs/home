# -*- coding: utf-8 -*-
# @File    : base_client.py
# @AUTH    : model_creater

import os
import thriftpy2
from ..client_pool import register_thrift_pool, get_thrift_pool

rpc_dir = os.path.abspath(os.path.dirname(__file__))
multimedia_thrift = thriftpy2.load(rpc_dir + "/protocols/main.thrift", module_name="multimedia_thrift")
register_thrift_pool('Multimedia', multimedia_thrift.MultimediaService, replace=False)

def create_artical(**kwargs):
    artical = multimedia_thrift.Artical()
    artical.__dict__.update(kwargs)
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.create_multimedia_artical(artical)
        return result


def update_artical(id, **kwargs):
    artical = multimedia_thrift.Artical()
    artical.__dict__.update(kwargs)
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.update_multimedia_artical(id, artical)
        return result


def delete_artical(id):
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.delete_multimedia_artical(id)
        return result


def select_artical(id):
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.select_multimedia_artical(id)
        if 0 == result.code and result.artical:
            result_object = result.artical
            result.artical = {
                "id": result_object.id,
                "title": artical.title,
                "author": artical.author,
                "year": artical.year,
                "source": artical.source,
                "summary": artical.summary,
                "content": artical.content,
                "ttype_id_list": artical.ttype_id_list,
                "tag_id_list": artical.tag_id_list,
                "comment_id_list": artical.comment_id_list,
            }
        return result


def search_artical():
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.list_multimedia_artical()
        result_object_list = []
        if 0 == result.code:
            for artical in result.artical_list:
                result_object_list.append({
                    "id": artical.id,
                    "title": artical.title,
                    "author": artical.author,
                    "year": artical.year,
                    "source": artical.source,
                    "summary": artical.summary,
                    "content": artical.content,
                    "ttype_id_list": artical.ttype_id_list,
                    "tag_id_list": artical.tag_id_list,
                    "comment_id_list": artical.comment_id_list,
                })
            result.artical_list = result_object_list
        return result

def create_movie(**kwargs):
    movie = multimedia_thrift.Movie()
    movie.__dict__.update(kwargs)
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.create_multimedia_movie(movie)
        return result


def update_movie(id, **kwargs):
    movie = multimedia_thrift.Movie()
    movie.__dict__.update(kwargs)
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.update_multimedia_movie(id, movie)
        return result


def delete_movie(id):
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.delete_multimedia_movie(id)
        return result


def select_movie(id):
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.select_multimedia_movie(id)
        if 0 == result.code and result.movie:
            result_object = result.movie
            result.movie = {
                "id": result_object.id,
                "title": movie.title,
                "year": movie.year,
                "summary": movie.summary,
            }
        return result


def search_movie():
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.list_multimedia_movie()
        result_object_list = []
        if 0 == result.code:
            for movie in result.movie_list:
                result_object_list.append({
                    "id": movie.id,
                    "title": movie.title,
                    "year": movie.year,
                    "summary": movie.summary,
                })
            result.movie_list = result_object_list
        return result

def create_tag(**kwargs):
    tag = multimedia_thrift.Tag()
    tag.__dict__.update(kwargs)
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.create_multimedia_tag(tag)
        return result


def update_tag(id, **kwargs):
    tag = multimedia_thrift.Tag()
    tag.__dict__.update(kwargs)
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.update_multimedia_tag(id, tag)
        return result


def delete_tag(id):
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.delete_multimedia_tag(id)
        return result


def select_tag(id):
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.select_multimedia_tag(id)
        if 0 == result.code and result.tag:
            result_object = result.tag
            result.tag = {
                "id": result_object.id,
                "name": tag.name,
                "color": tag.color,
            }
        return result


def search_tag():
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.list_multimedia_tag()
        result_object_list = []
        if 0 == result.code:
            for tag in result.tag_list:
                result_object_list.append({
                    "id": tag.id,
                    "name": tag.name,
                    "color": tag.color,
                })
            result.tag_list = result_object_list
        return result

def create_ttype(**kwargs):
    ttype = multimedia_thrift.Ttype()
    ttype.__dict__.update(kwargs)
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.create_multimedia_ttype(ttype)
        return result


def update_ttype(id, **kwargs):
    ttype = multimedia_thrift.Ttype()
    ttype.__dict__.update(kwargs)
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.update_multimedia_ttype(id, ttype)
        return result


def delete_ttype(id):
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.delete_multimedia_ttype(id)
        return result


def select_ttype(id):
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.select_multimedia_ttype(id)
        if 0 == result.code and result.ttype:
            result_object = result.ttype
            result.ttype = {
                "id": result_object.id,
                "name": ttype.name,
            }
        return result


def search_ttype():
    with get_thrift_pool('Multimedia').get_client() as client:
        result = client.list_multimedia_ttype()
        result_object_list = []
        if 0 == result.code:
            for ttype in result.ttype_list:
                result_object_list.append({
                    "id": ttype.id,
                    "name": ttype.name,
                })
            result.ttype_list = result_object_list
        return result

