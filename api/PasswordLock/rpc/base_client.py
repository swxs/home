# -*- coding: utf-8 -*-
# @File    : base_client.py
# @AUTH    : model_creater

import os
import thriftpy2
from rpc.pool import register_thrift_pool, get_thrift_pool

rpc_dir = os.path.abspath(os.path.dirname(__file__))
password_lock_thrift = thriftpy2.load(rpc_dir + "/protocols/main.thrift", module_name="password_lock_thrift")
register_thrift_pool('PasswordLock', password_lock_thrift.PasswordLockService, replace=False)

async def create_password_lock(**kwargs):
    password_lock = password_lock_thrift.model.PasswordLock()
    password_lock.__dict__.update(kwargs)
    async with get_thrift_pool('PasswordLock').get_client() as client:
        result = await client.create_password_lock_password_lock(password_lock)
        return result


async def update_password_lock(id, **kwargs):
    password_lock = password_lock_thrift.model.PasswordLock()
    password_lock.__dict__.update(kwargs)
    async with get_thrift_pool('PasswordLock').get_client() as client:
        result = await client.update_password_lock_password_lock(id, password_lock)
        return result


async def delete_password_lock(id):
    async with get_thrift_pool('PasswordLock').get_client() as client:
        result = await client.delete_password_lock_password_lock(id)
        return result


async def select_password_lock(id):
    async with get_thrift_pool('PasswordLock').get_client() as client:
        result = await client.select_password_lock_password_lock(id)
        if result.password_lock:
            result_object = result.password_lock
            if result_object:
                result.password_lock = {
                    "id": result_object.id,
                    "name": result_object.name,
                    "key": result_object.key,
                    "website": result_object.website,
                    "user_id": result_object.user_id,
                }
        return result


async def search_password_lock(search):
    async with get_thrift_pool('PasswordLock').get_client() as client:
        result = await client.search_password_lock_password_lock(search)
        result_object_list = []
        for password_lock in result.password_lock_list:
            result_object_list.append({
                "id": password_lock.id,
                "name": password_lock.name,
                "key": password_lock.key,
                "website": password_lock.website,
                "user_id": password_lock.user_id,
            })
        result.password_lock_list = result_object_list
        return result

