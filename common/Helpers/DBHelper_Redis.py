# coding=utf-8

import redis
import settings
from common.Helpers import DBHelper_Redis_LuaManager


class RedisDBHelper(object):
    def __init__(self, db, host, port, password):
        """
        连接数据库
        :param dbbase: 
        :param host: 
        :param port: 
        :param password: 
        """
        self.db = db
        self.host = host
        self.port = port
        self.password = password
        self._client = None
        self.LuaDict = {key: redis_lua(self.client) for key, redis_lua in DBHelper_Redis_LuaManager.LuaDict.items()}

    @property
    def client(self):
        if not self._client:
            self._client = redis.StrictRedis(host=self.host, port=self.port, db=self.db, password=self.password)
        return self._client

    def __getattribute__(self, item):
        if item in ["_client", "client", "db", "host", "port", "password", "get_next_seq", "run_script"]:
            return object.__getattribute__(self, item)
        return getattr(self.client, item)

    def get_next_seq(self, key):
        return self.client.incr(key, 1)

    def run_script(self, script_name, keys, args):
        """
        通用的脚本运行器
        :param script_name: 脚本名称
        :param keys: 可迭代对象（key1, key2...）
        :param args: 可迭代对象（key1, key2...）
        :return:
        """
        if script_name in self.LuaDict:
            return self.LuaDict[script_name].run_script(keys, args)
        else:
            raise Exception(u"暂时未定义该脚本")


redis_helper = RedisDBHelper(
    db=settings.REDIS_DB,
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD
)
