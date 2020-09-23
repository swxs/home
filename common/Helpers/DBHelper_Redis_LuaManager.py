# -*- coding: utf-8 -*-
# @File    : DBHelper_Redis_LuaManager.py
# @AUTH    : swxs
# @Time    : 2019/5/8 15:52

import hashlib


class LuaManager(type):
    def __new__(cls, name, bases, attrs):
        """
        lua:
        :param name:
        :param bases:
        :param attrs:
        :return:
        """
        attrs["flag"] = False
        attrs["lua"] = attrs.get("lua", b"")
        attrs["hashcode"] = hashlib.sha1(attrs.get("lua", b"")).hexdigest()
        return super(LuaManager, cls).__new__(cls, name, bases, attrs)


class RedisLua(object, metaclass=LuaManager):
    def __init__(self, rcon):
        self.rcon = rcon

    def run_script(self, keys, args):
        if self.flag or self.rcon.script_exists(self.hashcode)[0]:
            self.flag = True
            return self.rcon.evalsha(self.hashcode, len(keys), *(keys + args))
        else:
            return self.rcon.register_script(self.lua)(keys=keys, args=args)


class CheckProcessLua(RedisLua):
    lua = b"""\
    local data = false
    if( redis.call('exists', 'is_first_process') ~= 1 ) then
        redis.call('set', 'is_first_process', ARGV[1])
        redis.call('expire', 'is_first_process', 8*60*60)
        data = true
    end
    return data
    """


class IncrExpireLua(RedisLua):
    """
    给指定健设置过期时间， 过期时间不能被再次修改
    find in https://redis.io/commands/incr
    """

    lua = b"""\
    local current
    current = redis.call("incr", KEYS[1])
    if tonumber(current) == 1 then
        redis.call("expire", KEYS[1], ARGV[1])
    end
    return current
    """


class CountKeyWithPrefixLua(RedisLua):
    """
    扫描指定健(支持*)的数量
    """

    lua = b"""\
    local cursor = '0'
    local count = 0
    repeat
        local result = redis.call('SCAN', cursor, 'MATCH', KEYS[1], 'COUNT', 100)
        cursor = result[1]
        count = count + #result[2]
    until cursor == '0'
    return count
    """


class ScanDelWithPrefixLua(RedisLua):
    """
    删除指定健(支持*)， 并返回删除的数量
    """

    lua = b"""\
    redis.replicate_commands()
    local cursor = '0'
    local delete_count = 0
    repeat
        local result = redis.call('scan', cursor, 'MATCH', KEYS[1], 'COUNT', 100)
        cursor = result[1]
        local list = result[2]
        delete_count = delete_count + #list
        redis.call('del', unpack(list))
    until (cursor == '0')
    return delete_count
    """


LuaDict = {
    "IS_FIRST_PROCESS_LUA": CheckProcessLua,
    "INCR_EXPIRE_LUA": IncrExpireLua,
    "COUNT_KEY_WITH_PREFIX_LUA": CountKeyWithPrefixLua,
    "SCAN_DEL_WITH_PREFIXLUA": ScanDelWithPrefixLua,
}
