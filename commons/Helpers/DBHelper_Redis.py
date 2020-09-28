# coding=utf-8

import redis
import hashlib


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

    def run_script(self, lua, keys, args):
        """
        通用的脚本运行器
        :param lua: lua脚本代码 b''
        :param keys: 可迭代对象（key1, key2...）
        :param args: 可迭代对象（key1, key2...）
        :return:
        """
        hashcode = hashlib.sha1(lua).hexdigest()
        flag = self.scripts_map.get(hashcode, False)
        if not flag:
            hashcode = self.script_load(lua)
            self.scripts_map[hashcode] = True
        return self.evalsha(hashcode, keys, args)
