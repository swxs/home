# coding=utf-8

import redis
import settings
from common.Metaclass.Singleton import Singleton


class RedisDBHelper(object):
    __metaclass__ = Singleton

    def __init__(self,
                 dbbase=settings.REDIS_DB,
                 host=settings.REDIS_HOST,
                 port=settings.REDIS_PORT,
                 password=settings.REDIS_PASSWORD):
        '''
        连接数据库
        :param dbbase: 
        :param host: 
        :param port: 
        :param password: 
        '''
        self.client = redis.StrictRedis(host=host, port=port, db=dbbase, password=password)
