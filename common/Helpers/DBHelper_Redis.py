# coding=utf-8

import socket
import msgpack
import redis
import sys
import zlib
import settings


class RedisDBHelper(object):
    def __init__(self,
                 dbbase=settings.REDIS_DB,
                 host=settings.REDIS_HOST,
                 port=settings.REDIS_PORT,
                 password=settings.REDIS_PASSWORD):
        self.rcon = redis.StrictRedis(host=host, port=port, db=dbbase, password=password)
