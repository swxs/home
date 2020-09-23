import os
import asyncio
import uuid
from .DBHelper_Redis import redis_helper as redis


class CuckooFilter:
    """
    简介
    ----------
    布谷鸟过滤器

    """

    def __init__(self, key_name, number_of_buckets=2 ** 8, bucket_size=4, bits_per_fingerprint=8):
        """
        简介
        ----------
        设置过滤器属性

        参数
        ----------
        key_name :
            存放配置及数据的键
        number_of_buckets [可选]: 默认为 2**8 (> 2 and <= 2^29 : must be power of two (2^n))
            桶的数量
        bucket_size [可选]: 默认为 4 (>= 2 and <= 8)
            桶里的元素数量
        bits_per_fingerprint [可选]: 默认为 8
            指纹大小
        """
        self.key_name = key_name
        self.number_of_buckets = number_of_buckets
        self.bucket_size = bucket_size
        self.bits_per_fingerprint = bits_per_fingerprint

        self.initialed = False
        self.__init_cf_lua = None
        self.__insert_cf_lua = None
        self.__lookup_cf_lua = None
        self.__delete_cf_lua = None

    @property
    def init_cf_lua(self):
        if not self.__init_cf_lua:
            with open(os.path.join(os.path.dirname(__file__), "Lua", "cf_init.lua"), "rb") as fp:
                self.__init_cf_lua = fp.read()
        return self.__init_cf_lua

    @property
    def insert_cf_lua(self):
        if not self.__insert_cf_lua:
            with open(os.path.join(os.path.dirname(__file__), "Lua", "cf_insert.lua"), "rb") as fp:
                self.__insert_cf_lua = fp.read()
        return self.__insert_cf_lua

    @property
    def lookup_cf_lua(self):
        if not self.__lookup_cf_lua:
            with open(os.path.join(os.path.dirname(__file__), "Lua", "cf_lookup.lua"), "rb") as fp:
                self.__lookup_cf_lua = fp.read()
        return self.__lookup_cf_lua

    @property
    def delete_cf_lua(self):
        if not self.__delete_cf_lua:
            with open(os.path.join(os.path.dirname(__file__), "Lua", "cf_delete.lua"), "rb") as fp:
                self.__delete_cf_lua = fp.read()
        return self.__delete_cf_lua

    async def initial(self):
        if not self.initialed:
            await redis.run_script(
                self.init_cf_lua, [self.key_name], [self.number_of_buckets, self.bucket_size, self.bits_per_fingerprint]
            )
            print("initialed")
            self.initialed = True

    async def insert(self, value):
        await self.initial()
        result = await redis.run_script(self.insert_cf_lua, [self.key_name], [value])
        if result:
            return True
        else:
            return False

    async def lookup(self, value):
        await self.initial()
        result = await redis.run_script(self.lookup_cf_lua, [self.key_name], [value])
        if result:
            return True
        else:
            return False

    async def delete(self, value):
        await self.initial()
        result = await redis.run_script(self.delete_cf_lua, [self.key_name], [value])
        if result:
            return True
        else:
            return False


cuckoo_filter = CuckooFilter("CUCKOOFILTER", number_of_buckets=2 ** 16)
