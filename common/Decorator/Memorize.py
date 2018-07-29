# -*- coding: utf-8 -*-
# @File    : Memorize.py
# @AUTH    : swxs
# @Time    : 2018/7/28 21:22

import time
import threading
import hashlib
import settings
from common.Helpers.DBHelper_Memcache import MemcacheDBHelper
from common.Metaclass.Singleton import Singleton

__all__ = ["refresh", "memorize"]


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

    def get_main_key(self, obj):
        return f"{obj.__model_name__}, {obj.id}"

    def get_main_key_by_id(self, name, id):
        return f"{name}, {id}"

    def set_new_version(self, key):
        remote_version = memorize_helper.get_remote_obj_version(key)
        remote_version += 1
        memorize_helper.set_local_obj_version(key, remote_version)
        memorize_helper.set_remote_obj_version(key, remote_version)

    def make_main_memorize(self, obj):
        key = self.get_main_key(obj)
        self.OBJ_DICT[key] = obj
        self.set_new_version(key)

    def update_locale_memorize(self, obj, remote_version):
        key = self.get_main_key_by_id(obj)
        self.OBJ_DICT[key] = obj
        self.set_local_obj_version(key, remote_version)

    def get_main_memorize(self, model_name, id):
        pass

    def make_sub_memorize(self, key, obj):
        main_key = self.get_main_key(obj)
        self.OBJ_DICT[key] = main_key

        id_obj = self.OBJ_DICT.get(main_key, None)
        if id_obj is None:
            self.OBJ_DICT[main_key] = obj
            self.set_new_version(key)


memorize_helper = MemorizeHelper()


def clear(function):
    def helper(*args, **kwargs):
        key = memorize_helper.make_memcache_key(function, *args)
        ret_obj = function(*args, **kwargs)
        memorize_helper.set_local_obj_version(key, 0)
        memorize_helper.set_remote_obj_version(key, 0)
        return ret_obj

    return helper


def upgrade(function):
    def helper(*args, **kwargs):
        try:
            obj = function(*args, **kwargs)
        except:
            pass
        memorize_helper.make_main_memorize(obj)
        return obj

    return helper


def memorize(function):
    def helper(*args, **kwargs):

        def main_type(*args, **kwargs):
            remote_version = memorize_helper.get_remote_obj_version(key)
            if remote_version == 0:
                obj = function(*args, **kwargs)
                memorize_helper.make_main_memorize(obj)
            else:
                local_version = memorize_helper.get_local_obj_version(key)
                if local_version != remote_version:
                    obj = function(*args, **kwargs)
                    memorize_helper.update_locale_memorize(obj, remote_version)
                else:
                    if key in memorize_helper.OBJ_DICT:
                        obj = memorize_helper.OBJ_DICT[key]
                    else:
                        obj = function(*args, **kwargs)
                        memorize_helper.make_main_memorize(obj)
            return obj

        obj = None

        if "id" in kwargs:
            key = memorize_helper.get_main_key_by_id(args[0].__model_name__, kwargs.get("id"))

        else:
            key = memorize_helper.make_memcache_key(function, *args)
            remote_version = memorize_helper.get_remote_obj_version(key)
            if remote_version == 0:
                obj = function(*args, **kwargs)
                memorize_helper.OBJ_DICT[key] = obj
                memorize_helper.set_remote_obj_version(key, 1)
                memorize_helper.set_local_obj_version(key, 1)
            else:
                local_version = memorize_helper.get_local_obj_version(key)
                if local_version != remote_version:
                    obj = function(*args, **kwargs)
                    memorize_helper.OBJ_DICT[key] = obj
                    memorize_helper.set_local_obj_version(key, remote_version)
                else:
                    if key in memorize_helper.OBJ_DICT:
                        obj = memorize_helper.OBJ_DICT[key]
                    else:
                        obj = function(*args, **kwargs)
                        memorize_helper.OBJ_DICT[key] = obj

        return obj

    return helper
