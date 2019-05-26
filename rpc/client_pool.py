#!/usr/bin/python
import time
from thriftpy2.rpc import make_aio_client
from common.Exceptions import ApiException
import settings


class ThriftClient(object):
    """
    保存Thrift客户端连接信息
    """

    def __init__(self, client, timeout, pool=None):
        """
        @param client: thriftpy2的客户端对象
        @param expire: 客户端连接超时时间，=connect_time+timeout
        """
        self._client = client
        self._pool = pool
        self.set_expire(timeout)

    def is_valid(self):
        if self._expire and time.time() >= self._expire:
            # 连接超时
            return False
        return self._client._iprot.trans._trans.is_open

    def set_expire(self, timeout):
        """
        @param timeout: 超时时间，单位：秒
        """
        if timeout:
            self._expire = time.time() + timeout
        else:
            self._expire = None

    def close(self):
        self._client.close()


class ThriftClientMgr(object):
    def __init__(self, pool=None):
        self._pool = pool

    async def __aenter__(self):
        client = await self._pool._get_client()
        self._client = client
        return client._client

    async def __aexit__(self, exc_cls, exc_obj, tb):
        client = self._client
        if client:
            if self._pool and client.is_valid():
                if exc_obj and not isinstance(exc_obj, ApiException):
                    client.close()
                else:
                    self._pool.push_client(client)
            else:
                client.close()


class ThriftClientPool(object):
    """
    Thrift客户端连接池
    """

    def __init__(self, service, host, port, timeout=None):
        """
        @param service: thrift_client的服务接口
        @param host: 服务端地址
        @param port: 服务端端口
        @param timeout: 超时时间，　单位：毫秒
        """
        self._host = host
        self._port = port
        self._service = service
        if timeout:
            self._timeout = timeout / 1000.0
        else:
            self._timeout = None
        self._connections = []

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    def _get_valid_client(self):
        while self._connections:
            c = self._connections.pop()
            if c.is_valid():
                return c
            else:
                c.close()

    async def _make_client(self):
        client = await make_aio_client(self._service, self._host, self._port, socket_timeout=self._timeout)
        return ThriftClient(client, self._timeout)

    async def _get_client(self):
        c = self._get_valid_client()
        if not c:
            c = await self._make_client()
        return c

    def get_client(self):
        """
        配合上下文管理器使用
        """
        return ThriftClientMgr(pool=self)

    def push_client(self, client):
        client.set_expire(self._timeout)
        self._connections.append(client)

    def reset(self):
        while True:
            c = self._get_valid_client()
            if c is None:
                return
            c.close()


__Thrift_Pools = {}


def register_thrift_pool(name, service, host=None, port=None, timeout=None, replace=True):
    global __Thrift_Pools
    if name not in __Thrift_Pools or replace:
        if not host:
            host = get_rpc_server_ip(name)
        if not port:
            port = get_rpc_server_port(name)
        __Thrift_Pools[name] = ThriftClientPool(
            service, host, port, timeout=timeout)


def get_rpc_server_ip(name):
    """
    根据子系统名获取rpc服务ip
    """
    return getattr(settings, name.upper() + '_RPC_SERVER_HOST', settings.RPC_SERVER_HOST)


def get_rpc_server_port(name):
    """
    根据子系统名获取rpc服务ip
    """
    return getattr(settings, name.upper() + '_RPC_SERVER_PORT', settings.RPC_SERVER_PORT)


def get_thrift_pool(name):
    return __Thrift_Pools.get(name)


def clear_all_pools():
    for pool in __Thrift_Pools.values():
        pool.reset()
