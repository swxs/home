# -*- coding: utf-8 -*-
# @File    : base_client.py
# @AUTH    : model_creater

import os
import thriftpy2
from ..client_pool import register_thrift_pool, get_thrift_pool

rpc_dir = os.path.abspath(os.path.dirname(__file__))
user_thrift = thriftpy2.load(rpc_dir + "/protocols/main.thrift", module_name="user_thrift")
register_thrift_pool('User', user_thrift.UserService, replace=False)

def create_user(**kwargs):
    user = user_thrift.User()
    user.__dict__.update(kwargs)
    with get_thrift_pool('User').get_client() as client:
        result = client.create_user_user(user)
        return result


def update_user(id, **kwargs):
    user = user_thrift.User()
    user.__dict__.update(kwargs)
    with get_thrift_pool('User').get_client() as client:
        result = client.update_user_user(id, user)
        return result


def delete_user(id):
    with get_thrift_pool('User').get_client() as client:
        result = client.delete_user_user(id)
        return result


def select_user(id):
    with get_thrift_pool('User').get_client() as client:
        result = client.select_user_user(id)
        if 0 == result.code and result.user:
            result_object = result.user
            result.user = {
                "id": result_object.id,
                "username": user.username,
                "nickname": user.nickname,
                "password": user.password,
                "salt": user.salt,
                "avatar": user.avatar,
                "email": user.email,
                "mobile": user.mobile,
                "description": user.description,
            }
        return result


def search_user():
    with get_thrift_pool('User').get_client() as client:
        result = client.list_user_user()
        result_object_list = []
        if 0 == result.code:
            for user in result.user_list:
                result_object_list.append({
                    "id": user.id,
                    "username": user.username,
                    "nickname": user.nickname,
                    "password": user.password,
                    "salt": user.salt,
                    "avatar": user.avatar,
                    "email": user.email,
                    "mobile": user.mobile,
                    "description": user.description,
                })
            result.user_list = result_object_list
        return result

def create_description(**kwargs):
    description = user_thrift.Description()
    description.__dict__.update(kwargs)
    with get_thrift_pool('User').get_client() as client:
        result = client.create_user_description(description)
        return result


def update_description(id, **kwargs):
    description = user_thrift.Description()
    description.__dict__.update(kwargs)
    with get_thrift_pool('User').get_client() as client:
        result = client.update_user_description(id, description)
        return result


def delete_description(id):
    with get_thrift_pool('User').get_client() as client:
        result = client.delete_user_description(id)
        return result


def select_description(id):
    with get_thrift_pool('User').get_client() as client:
        result = client.select_user_description(id)
        if 0 == result.code and result.description:
            result_object = result.description
            result.description = {
                "id": result_object.id,
            }
        return result


def search_description():
    with get_thrift_pool('User').get_client() as client:
        result = client.list_user_description()
        result_object_list = []
        if 0 == result.code:
            for description in result.description_list:
                result_object_list.append({
                    "id": description.id,
                })
            result.description_list = result_object_list
        return result

