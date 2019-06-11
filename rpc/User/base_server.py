# -*- coding: utf-8 -*-
# @File    : base_server.py
# @AUTH    : model_creater

import os
import json
import thriftpy2
from thriftpy2.rpc import make_server
from rpc.utils import render_thrift
from api.User.utils.User import User
from api.User.utils.User import User


rpc_dir = os.path.abspath(os.path.dirname(__file__))
user_thrift = thriftpy2.load(rpc_dir + "/protocols/main.thrift", module_name="user_thrift")

class BaseDispatcher(object):
    @render_thrift(user_thrift.CreateResult)
    def create_user_user(self, **kwargs):
        result = user_thrift.CreateResult
        user = User.create(**kwargs)
        result.id = user.id
        result.code = 0
        return result

    @render_thrift(user_thrift.UpdateResult)
    def update_user_user(self, user_id, **kwargs):
        result = user_thrift.UpdateResult()
        user = User.select(id=user_id)
        user = user.update(**kwargs)
        result.id = user.id
        result.code = 0
        return result

    @render_thrift(user_thrift.DeleteResult)
    def delete_user_user(self, user_id):
        result = user_thrift.DeleteResult()
        user = User.select(id=user_id)
        user.delete()
        result.code = 0
        return result

    @render_thrift(user_thrift.UserResult)
    def select_user_user(self, user_id):
        result = user_thrift.UserResult()
        user = User.select(id=user_id)
        result_object = user_thrift.user
        result_object.id = str(user.id)
        result_object.username = user.username
        result_object.nickname = user.nickname
        result_object.password = user.password
        result_object.salt = user.salt
        result_object.avatar = user.avatar
        result_object.email = user.email
        result_object.mobile = user.mobile
        result_object.description = user.description
        result.user = result_object
        result.code = 0
        return result

    @render_thrift(user_thrift.UserSearchResult)
    def list_user_user(self):
        result = user_thrift.UserSearchResult()
        user_list = User.filter()
        result_object_list = []
        for user in user_list:
            result_object = user_thrift.user
            result_object.id = str(user.id)
            result_object.username = user.username
            result_object.nickname = user.nickname
            result_object.password = user.password
            result_object.salt = user.salt
            result_object.avatar = user.avatar
            result_object.email = user.email
            result_object.mobile = user.mobile
            result_object.description = user.description
            result_object_list.append(result_object)
        result.code = 0
        result.user_list = result_object_list
        return result

    @render_thrift(user_thrift.CreateResult)
    def create_user_description(self, **kwargs):
        result = user_thrift.CreateResult
        description = Description.create(**kwargs)
        result.id = description.id
        result.code = 0
        return result

    @render_thrift(user_thrift.UpdateResult)
    def update_user_description(self, description_id, **kwargs):
        result = user_thrift.UpdateResult()
        description = Description.select(id=description_id)
        description = description.update(**kwargs)
        result.id = description.id
        result.code = 0
        return result

    @render_thrift(user_thrift.DeleteResult)
    def delete_user_description(self, description_id):
        result = user_thrift.DeleteResult()
        description = Description.select(id=description_id)
        description.delete()
        result.code = 0
        return result

    @render_thrift(user_thrift.DescriptionResult)
    def select_user_description(self, description_id):
        result = description_thrift.DescriptionResult()
        description = Description.select(id=description_id)
        result_object = user_thrift.description
        result_object.id = str(description.id)
        result. = result_object
        result.code = 0
        return result

    @render_thrift(user_thrift.SearchResult)
    def list_user_(self):
        result = user_thrift.SearchResult()
        _list = Description.filter()
        result_object_list = []
        for  in _list:
            result_object = user_thrift.description
            result_object.id = str(description.id)
            result_object_list.append(result_object)
        result.code = 0
        result.description_list = result_object_list
        return result



if __name__ == '__main__':
    from ..client_pool import get_rpc_server_host, get_rpc_server_port

    server = make_server(
        user_thrift.UserService,
        BaseDispatcher(),
        get_rpc_server_host('User'),
        get_rpc_server_port('User'),
        client_timeout=None
    )
    server.serve()