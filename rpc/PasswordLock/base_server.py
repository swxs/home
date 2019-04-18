# -*- coding: utf-8 -*-
# @File    : base_server.py
# @AUTH    : model_creater

import os
import json
import thriftpy2
from thriftpy2.rpc import make_server
from rpc.utils import render_thrift
from api.PasswordLock.utils.PasswordLock import PasswordLock


rpc_dir = os.path.abspath(os.path.dirname(__file__))
password_lock_thrift = thriftpy2.load(rpc_dir + "/protocols/main.thrift", module_name="password_lock_thrift")

class BaseDispatcher(object):
    @render_thrift(password_lock_thrift.CreateResult)
    def create_password_lock_password_lock(self, **kwargs):
        result = password_lock_thrift.CreateResult
        password_lock = PasswordLock.create(**kwargs)
        result.id = password_lock.id
        result.code = 0
        return result

    @render_thrift(password_lock_thrift.UpdateResult)
    def update_password_lock_password_lock(self, password_lock_id, **kwargs):
        result = password_lock_thrift.UpdateResult()
        password_lock = PasswordLock.select(id=password_lock_id)
        password_lock = password_lock.update(**kwargs)
        result.id = password_lock.id
        result.code = 0
        return result

    @render_thrift(password_lock_thrift.DeleteResult)
    def delete_password_lock_password_lock(self, password_lock_id):
        result = password_lock_thrift.DeleteResult()
        password_lock = PasswordLock.select(id=password_lock_id)
        password_lock.delete()
        result.code = 0
        return result

    @render_thrift(password_lock_thrift.PasswordLockResult)
    def select_password_lock_password_lock(self, password_lock_id):
        result = password_lock_thrift.PasswordLockResult()
        password_lock = PasswordLock.select(id=password_lock_id)
        result_object = password_lock_thrift.password_lock
        result_object.id = str(password_lock.id)
        result_object.name = password_lock.name
        result_object.key = password_lock.key
        result_object.website = password_lock.website
        result_object.user_id = str(password_lock.user_id)
        result.password_lock = result_object
        result.code = 0
        return result

    @render_thrift(password_lock_thrift.PasswordLockSearchResult)
    def list_password_lock_password_lock(self):
        result = password_lock_thrift.PasswordLockSearchResult()
        password_lock_list = PasswordLock.filter()
        result_object_list = []
        for password_lock in password_lock_list:
            result_object = password_lock_thrift.password_lock
            result_object.id = str(password_lock.id)
            result_object.name = password_lock.name
            result_object.key = password_lock.key
            result_object.website = password_lock.website
            result_object.user_id = str(password_lock.user_id)
            result_object_list.append(result_object)
        result.code = 0
        result.password_lock_list = result_object_list
        return result



if __name__ == '__main__':
    from ..client_pool import get_rpc_server_host, get_rpc_server_port

    server = make_server(
        password_lock_thrift.PasswordLockService,
        BaseDispatcher(),
        get_rpc_server_host('PasswordLock'),
        get_rpc_server_port('PasswordLock'),
        client_timeout=None
    )
    server.serve()