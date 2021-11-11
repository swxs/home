# -*- coding: utf-8 -*-
# @File    : memorizer_cache.py
# @AUTH    : swxs
# @Time    : 2018/7/28 21:22

import time
import uuid
import logging
import threading
import hashlib
import weakref
from functools import wraps
from commons.Helpers import memcache_helper

logger = logging.getLogger("main.dao.memorize")

__all__ = ["clear", "upgrade", "cache", "memorize"]


class LocalMemorizer:
    name = "local"

    def __init__(self):
        self.OBJ_VERSION_DICT = {}
        self.OBJ_DICT = {}
        self.OBJ_EXPIRE_DICT = {}
        self.OBJ_DICT2 = {}
        self.OBJ_EXPIRE_DICT2 = {}
        self.DEFAULT_EXPIRE_SECONDS = 300
        self.DEFAULT_VERSION_EXPIRE_SECONDS = 60 * 60 * 24
        self.MEMORY_CLEANER_PERIOD = 600
        self.memcache_helper = memcache_helper
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
            # logger.debug('%s keys deleted, %s keys remain' % (len(keys_to_remove), len(OBJ_DICT)),)

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
                    # logger.debug('%s keys deleted, %s keys remain' % (len(keys_to_remove), len(OBJ_DICT)),)

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
            lis = [kwargs[k] for k in sorted(kwargs.keys()) if kwargs[k] not in (None, )]
            return md5(''.join(lis))

        return f"{_model_name}_{_open_api_signature(**kwargs)}"
