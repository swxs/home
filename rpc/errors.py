#!/usr/bin/python

"""
API调用过程中进行RPC调用时RPC框架报错的错误码
"""


class RPCError(Exception):
    pass


class NetworkTimeout(RPCError):
    pass


class AutoReconnect(RPCError):
    pass
