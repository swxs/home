# -*- coding: utf-8 -*-
# @File    : Memorize.py
# @AUTH    : swxs
# @Time    : 2018/7/28 21:22

import time
import uuid
import threading
import hashlib
import weakref
from functools import wraps
from common.Helpers.DBHelper_Memcache import MemcacheDBHelper
from common.Metaclass.Singleton import Singleton
from common.Utils.log_utils import getLogger
from api.BaseConsts import undefined

log = getLogger("memorize")

__all__ = ["clear", "upgrade", "cache", "memorize"]


class MemorizeHelper():
    __metaclass__ = Singleton

    def __init__(self):
        self.OBJ_VERSION_DICT = {}
        self.OBJ_DICT = {}
        self.OBJ_EXPIRE_DICT = {}
        self.OBJ_DICT2 = {}
        self.OBJ_EXPIRE_DICT2 = {}
        self.DEFAULT_EXPIRE_SECONDS = 300
        self.DEFAULT_VERSION_EXPIRE_SECONDS = 60 * 60 * 24
        self.MEMORY_CLEANER_PERIOD = 600
        self.memcache_helper = MemcacheDBHelper()
        self.memory_cleaner_thread_started = False
        self.start_memory_cleaner_thread()

    def set_local_obj_version(self, key, version):
        self.OBJ_VERSION_DICT[key] = version

    def get_local_obj_version(self, key):
        return self.OBJ_VERSION_DICT.get(key) or 0

    def set_remote_obj_version(self, key, version):
        return self.memcache_helper.set(str(key), version, self.DEFAULT_VERSION_EXPIRE_SECONDS)

    def get_remote_obj_version(self, key):
        return self.memcache_helper.get(str(key)) or 0

    def clear_key(self, key):
        try:
            del self.OBJ_DICT[key]
            del self.OBJ_EXPIRE_DICT[key]
            del self.OBJ_VERSION_DICT[key]
        except KeyError:
            pass
            # log.debug('%s keys deleted, %s keys remain' % (len(keys_to_remove), len(OBJ_DICT)),)

    def version_expired(self, key):
        local_version = self.get_local_obj_version(key)
        remote_version = self.get_remote_obj_version(key)
        return local_version != remote_version

    def start_memory_cleaner_thread(self):
        if not self.memory_cleaner_thread_started:
            threading.Thread(target=self.start_memory_cleaner, args=(), name='memory_cleaner_thread').start()
            self.memory_cleaner_thread_started = True

    def start_memory_cleaner(self):
        while True:
            time.sleep(self.MEMORY_CLEANER_PERIOD)
            keys_to_remove = []
            for key, value in self.OBJ_EXPIRE_DICT.items():
                if self.OBJ_EXPIRE_DICT[key] < int(round(time.time())):
                    keys_to_remove.append(key)
            for key in keys_to_remove:
                try:
                    del self.OBJ_DICT[key]
                    del self.OBJ_EXPIRE_DICT[key]
                    del self.OBJ_VERSION_DICT[key]
                except KeyError:
                    pass
                    # log.debug('%s keys deleted, %s keys remain' % (len(keys_to_remove), len(OBJ_DICT)),)

    def make_memcache_key(self, function, *args):
        args_str = []
        for arg in args:
            if isinstance(arg, str):
                args_str.append(arg.encode('utf-8'))
            else:
                args_str.append(str(arg))

        return function.__name__ + hashlib.md5('#'.join(args_str)).hexdigest()

    def set_obj_new_version(self, obj, key, remote_version=None):
        self.OBJ_DICT[key] = obj
        if remote_version is None:
            # remote_version = self.get_remote_obj_version(key)
            # remote_version += 1
            remote_version = str(uuid.uuid4())
        self.set_local_obj_version(key, remote_version)
        self.set_remote_obj_version(key, remote_version)
        return remote_version

    def make_model_main_key(self, name, id):
        return f"{name}_{id}"

    def make_model_sub_key(self, _model_name, **kwargs):
        def md5(raw_str):
            if isinstance(raw_str, str):
                raw_str = raw_str.encode('utf-8')
            return hashlib.md5(raw_str).hexdigest()

        def _open_api_signature(**kwargs):
            lis = [kwargs[k] for k in sorted(kwargs.keys()) if kwargs[k] not in [None, undefined]]
            return md5(''.join(lis))

        return f"{_model_name}_{_open_api_signature(**kwargs)}"


memorize_helper = MemorizeHelper()


def clear(function):
    @wraps(function)
    def helper(*args, **kwargs):
        obj = args[0]
        key = memorize_helper.make_model_main_key(obj.__model_name__, obj.id)
        try:
            obj = function(*args, **kwargs)
        except Exception as e:
            raise e
        memorize_helper.clear_key(key)
        memorize_helper.set_obj_new_version(obj, key, 0)
        return obj

    return helper


def upgrade(function):
    @wraps(function)
    def helper(*args, **kwargs):
        try:
            obj = function(*args, **kwargs)
        except Exception as e:
            raise e
        key = memorize_helper.make_model_main_key(obj.__model_name__, obj.id)
        memorize_helper.clear_key(key)
        remote_version = memorize_helper.set_obj_new_version(obj, key)
        obj.__version__ = remote_version
        return obj

    return helper


def cache(function):
    @wraps(function)
    def helper(*args, **kwargs):
        if "id" in kwargs:
            key = memorize_helper.make_model_main_key(args[0].__model_name__, kwargs.get("id"))  # 获取key
            remote_version = memorize_helper.get_remote_obj_version(key)  # 获取当前版本号
            if remote_version == 0:  # 如果远程无版本
                obj = function(*args, **kwargs)  # 查询获取对象
                remote_version = memorize_helper.set_obj_new_version(obj, key)  # 创建缓存， 并同步到远程
            else:  # 如果远程有版本
                local_version = memorize_helper.get_local_obj_version(key)  # 获取当前版本
                if local_version != remote_version:  # 当前版本与远程版本不同
                    obj = function(*args, **kwargs)  # 查询获取对象
                    remote_version = memorize_helper.set_obj_new_version(obj, key, remote_version)  # 同步版本至远程版本
                else:  # 版本相同
                    if key in memorize_helper.OBJ_DICT:  # key 存在
                        obj = memorize_helper.OBJ_DICT[key]  # 获取缓存对象
                    else:  # key 不存在, 可能被删掉了？
                        obj = function(*args, **kwargs)  # 查询获取对象
                        remote_version = memorize_helper.set_obj_new_version(obj, key)  # 创建缓存， 并同步到远程
            obj.__version__ = remote_version
            return memorize_helper.OBJ_DICT[key]
        else:
            sub_key = memorize_helper.make_model_sub_key(args[0].__model_name__, **kwargs)  # 获取key

            new_obj = False
            if sub_key in memorize_helper.OBJ_DICT:
                obj = memorize_helper.OBJ_DICT[sub_key]
                try:
                    print(obj.id)
                except:
                    obj = function(*args, **kwargs)  # 查询获取对象
                    new_obj = True
            else:
                obj = function(*args, **kwargs)  # 查询获取对象
                new_obj = True

            key = memorize_helper.make_model_main_key(obj.__model_name__, obj.id)  # 获取key

            remote_version = memorize_helper.get_remote_obj_version(key)  # 获取当前版本号
            if remote_version == 0:  # 如果远程无版本
                remote_version = memorize_helper.set_obj_new_version(obj, key)  # 创建缓存， 并同步到远程
            else:  # 如果远程有版本
                local_version = memorize_helper.get_local_obj_version(key)  # 获取当前版本
                if local_version != remote_version:  # 当前版本与远程版本不同
                    if not new_obj:
                        obj = function(*args, **kwargs)  # 查询获取对象
                    remote_version = memorize_helper.set_obj_new_version(obj, key, remote_version)  # 同步版本至远程版本
                else:  # 版本相同
                    if key in memorize_helper.OBJ_DICT:  # key 存在
                        obj = memorize_helper.OBJ_DICT[key]  # 获取缓存对象
                    else:  # key 不存在, 可能被删掉了？
                        if not new_obj:
                            obj = function(*args, **kwargs)  # 查询获取对象
                        remote_version = memorize_helper.set_obj_new_version(obj, key)  # 创建缓存， 并同步到远程
            memorize_helper.OBJ_DICT[sub_key] = weakref.proxy(memorize_helper.OBJ_DICT[key])
            obj.__version__ = remote_version
            return memorize_helper.OBJ_DICT[key]

    return helper


def memorize(function):
    @wraps(function)
    def helper(*args, **kwargs):
        key = memorize_helper.make_memcache_key(function, *args)  # 获取key
        remote_version = memorize_helper.get_remote_obj_version(key)  # 获取当前版本号
        if remote_version == 0:  # 如果远程无版本
            obj = function(*args, **kwargs)  # 查询获取对象
            memorize_helper.set_obj_new_version(obj, key)  # 创建缓存， 并同步到远程
        else:  # 如果远程有版本
            local_version = memorize_helper.get_local_obj_version(key)  # 获取当前版本
            if local_version != remote_version:  # 当前版本与远程版本不同
                obj = function(*args, **kwargs)  # 查询获取对象
                memorize_helper.set_obj_new_version(obj, key, remote_version)  # 同步版本至远程版本
            else:  # 版本相同
                if key in memorize_helper.OBJ_DICT:  # key 存在
                    obj = memorize_helper.OBJ_DICT[key]  # 获取缓存对象
                else:  # key 不存在, 可能被删掉了？
                    obj = function(*args, **kwargs)  # 查询获取对象
                    memorize_helper.set_obj_new_version(obj, key)  # 创建缓存， 并同步到远程
        return obj

    return helper
