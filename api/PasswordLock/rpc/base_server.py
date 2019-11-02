# -*- coding: utf-8 -*-
# @File    : base_server.py
# @AUTH    : model_creater

import os
import json
import thriftpy2
from common.Decorator.render import render_thrift
from api.PasswordLock.utils.PasswordLock import PasswordLock
from rpc.dispatcher import BaseDispatcher


rpc_dir = os.path.abspath(os.path.dirname(__file__))
password_lock_thrift = thriftpy2.load(rpc_dir + "/protocols/main.thrift", module_name="password_lock_thrift")

class Dispatcher(BaseDispatcher):
    @render_thrift(password_lock_thrift.model.CreateResult)
    async def create_password_lock_password_lock(self, **kwargs):
        result = password_lock_thrift.CreateResult()
        password_lock = await PasswordLock.create(**kwargs)
        result.code = 0
        result.msg = ""
        result.id = password_lock.id
        return result

    @render_thrift(password_lock_thrift.model.UpdateResult)
    async def update_password_lock_password_lock(self, id, **kwargs):
        result = password_lock_thrift.model.UpdateResult()
        password_lock = await PasswordLock.select(id=id)
        password_lock = await password_lock.update(**kwargs)
        result.code = 0
        result.msg = ""
        result.id = password_lock.id
        return result

    @render_thrift(password_lock_thrift.model.DeleteResult)
    async def delete_password_lock_password_lock(self, id):
        result = password_lock_thrift.model.DeleteResult()
        password_lock = await PasswordLock.select(id=id)
        await password_lock.delete()
        result.code = 0
        result.msg = ""
        result.count = 0
        return result

    @render_thrift(password_lock_thrift.model.SelectPasswordLockResult)
    async def select_password_lock_password_lock(self, id):
        result = password_lock_thrift.model.SelectPasswordLockResult()
        password_lock = await PasswordLock.select(id=id)
        result_object = password_lock_thrift.model.PasswordLock()
        result_object.id = str(password_lock.id)
        result_object.name = password_lock.name
        result_object.key = password_lock.key
        result_object.website = password_lock.website
        result_object.user_id = str(password_lock.user_id)
        result.code = 0
        result.msg = ""
        result.password_lock = result_object
        return result

    @render_thrift(password_lock_thrift.model.SearchPasswordLockResult)
    async def search_password_lock_password_lock(self, search):
        result = password_lock_thrift.model.SearchPasswordLockResult()
        password_lock_list = PasswordLock.search()
        result_object_list = []
        async for password_lock in password_lock_list:
            result_object = password_lock_thrift.model.PasswordLock()
            result_object.id = str(password_lock.id)
            result_object.name = password_lock.name
            result_object.key = password_lock.key
            result_object.website = password_lock.website
            result_object.user_id = str(password_lock.user_id)
            result_object_list.append(result_object)
        result.code = 0
        result.msg = ""
        result.password_lock_list = result_object_list
        return result



if __name__ == '__main__':
    from rpc.main import make_server
    server = make_server(
        port=5000,
        module_list=['api.PasswordLock.rpc.base_server']
    )
    server.serve()