# -*- coding: utf-8 -*-
# @File    : DBHelper_Memcache.py
# @AUTH    : swxs
# @Time    : 2018/7/28 21:24

import memcache
import settings
from common.Metaclass.Singleton import Singleton


class MemcacheDBHelper(object):
    __metaclass__ = Singleton

    def __init__(self, host=settings.MEMCACHE_HOST, port=settings.MEMCACHE_PORT):
        """
        连接数据库
        :param host:
        :param port:
        """
        self.client = memcache.Client([f"{host}:{port}"])

    def set(self, key, value, time=settings.MEMCACHE_EXPIRE_TIME):
        """time为过期时间，以秒为单位"""
        return self.client.set(str(key), value, time)

    def get(self, key):
        return self.client.get(str(key))
