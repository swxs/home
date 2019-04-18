# -*- coding: utf-8 -*-
# @File    : base_client.py
# @AUTH    : model_creater

import os
import thriftpy2
from ..client_pool import register_thrift_pool, get_thrift_pool

rpc_dir = os.path.abspath(os.path.dirname(__file__))
password_lock_thrift = thriftpy2.load(rpc_dir + "/protocols/main.thrift", module_name="password_lock_thrift")
register_thrift_pool('PasswordLock', password_lock_thrift.PasswordLockService, replace=False)

def create_password_lock(**kwargs):
    password_lock = password_lock_thrift.PasswordLock()
    password_lock.__dict__.update(kwargs)
    with get_thrift_pool('PasswordLock').get_client() as client:
        result = client.create_password_lock_password_lock(password_lock)
        return result


def update_password_lock(id, **kwargs):
    password_lock = password_lock_thrift.PasswordLock()
    password_lock.__dict__.update(kwargs)
    with get_thrift_pool('PasswordLock').get_client() as client:
        result = client.update_password_lock_password_lock(id, password_lock)
        return result


def delete_password_lock(id):
    with get_thrift_pool('PasswordLock').get_client() as client:
        result = client.delete_password_lock_password_lock(id)
        return result


def select_password_lock(id):
    with get_thrift_pool('PasswordLock').get_client() as client:
        result = client.select_password_lock_password_lock(id)
        if 0 == result.code and result.password_lock:
            result_object = result.password_lock
            result.password_lock = {
                "id": result_object.id,
                "name": password_lock.name,
                "key": password_lock.key,
                "website": password_lock.website,
                "user_id": password_lock.user_id,
            }
        return result


def list_password_lock():
    with get_thrift_pool('PasswordLock').get_client() as client:
        result = client.list_password_lock_password_lock()
        result_object_list = []
        if 0 == result.code:
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
