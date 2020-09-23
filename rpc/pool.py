import os
import socket
import time
import asyncio
import threading
import collections
from _ssl import SSLError
from async_generator import asynccontextmanager
from asyncio.streams import _DEFAULT_LIMIT, StreamReader, StreamReaderProtocol, StreamWriter
from thriftpy2.contrib.aio.client import TAsyncClient
from thriftpy2.contrib.aio.protocol.binary import TAsyncBinaryProtocolFactory
from thriftpy2.contrib.aio.transport.buffered import TAsyncBufferedTransportFactory
from thriftpy2.contrib.aio.socket import TAsyncSocket
from .errors import NetworkTimeout, AutoReconnect


async def _create_connection(host, port, options):
    client = TAsyncSocket(
        host,
        port,
        socket_timeout=options.socket_timeout,
        connect_timeout=options.connect_timeout,
        cafile=options.cafile,
        ssl_context=options.ssl_context,
        certfile=options.certfile,
        keyfile=options.keyfile,
        validate=options.validate,
    )
    transport = options.trans_factory.get_transport(client)
    protocol = options.proto_factory.get_protocol(transport)
    await transport.open()
    client = TAsyncClient(options.service, protocol)
    return client


def _raise_connection_failure(host, port, error):
    msg = f'{host}:{port}: {error}'
    if isinstance(error, socket.timeout):
        raise NetworkTimeout(msg)
    elif isinstance(error, SSLError) and 'timed out' in str(error):
        raise NetworkTimeout(msg)
    else:
        raise AutoReconnect(msg)


class ClientInfo(object):
    def __init__(self, client, pool, host, port, id):
        self.client = client
        self.pool = pool
        self.host = host
        self.port = port
        self.id = id
        self.closed = False

    @property
    def pool_id(self):
        return self.pool.pool_id

    def close_client(self, message=None):
        self.client.close()

    def update_last_checkin_time(self):
        pass

    def __eq__(self, other):
        return self.client == other.client

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.client)

    def __repr__(self):
        return "ClientInfo(%s)%s at %s" % (repr(self.client), self.closed and " CLOSED" or "", id(self))


class PoolOptions(object):
    def __init__(self, service=None):
        self.socket_timeout = None
        self.connect_timeout = None
        self.cafile = None
        self.ssl_context = None
        self.certfile = None
        self.keyfile = None
        self.validate = True
        self.trans_factory = TAsyncBufferedTransportFactory()
        self.proto_factory = TAsyncBinaryProtocolFactory()
        self.service = service


class Pool(object):
    def __init__(self, host, port, **kwargs):
        self.clients = collections.deque()
        self.lock = threading.Lock()
        self.active_clients = 0
        self.next_connection_id = 1
        self.closed = False

        self.pool_id = 0
        self.pid = os.getpid()
        self.host = host
        self.port = port
        self.options = PoolOptions(**kwargs)

    def _reset(self, close):
        with self.lock:
            if self.closed:
                return
            self.pool_id += 1
            self.pid = os.getpid()

            clients, self.clients = self.clients, collections.deque()
            self.active_clients = 0
            if close:
                self.closed = True

        if close:
            for client_info in clients:
                client_info.close_client()
        else:
            for client_info in clients:
                client_info.close_client()

    def reset(self):
        return self._reset(close=True)

    def close(self):
        return self._reset(close=False)

    async def connect(self):
        with self.lock:
            connection_id = self.next_connection_id
            self.next_connection_id += 1

        client = None
        try:
            client = await _create_connection(self.host, self.port, self.options)
        except socket.error as error:
            if client is not None:
                client.close()
            _raise_connection_failure(self.host, self.port, error)

        client_info = ClientInfo(client, self, self.host, self.port, connection_id)
        return client_info

    async def _get_client(self):
        if self.pid != os.getpid():
            self.reset()

        if self.closed:
            raise Exception('Attempted to check out a connection from closed connection pool')

        with self.lock:
            self.active_clients += 1

        try:
            client_info = None
            while client_info is None:
                try:
                    with self.lock:
                        client_info = self.clients.popleft()
                except IndexError:
                    client_info = await self.connect()
                else:
                    if self._perished(client_info):
                        client_info = None

        except Exception:
            with self.lock:
                self.active_clients -= 1
            raise

        return client_info

    @asynccontextmanager
    async def get_client(self):
        client_info = await self._get_client()
        yield client_info.client
        self.return_client(client_info)

    def return_client(self, client_info):
        if self.pid != os.getpid():
            self.reset()
        else:
            if self.closed:
                client_info.close_client()
            elif client_info.pool_id != self.pool_id:
                client_info.close_client()
            elif not client_info.closed:
                client_info.update_last_checkin_time()
                with self.lock:
                    self.clients.appendleft(client_info)

        with self.lock:
            self.active_clients -= 1

    def _perished(self, client_info):
        idle_time_seconds = client_info.idle_time_seconds()
        if (self.options.max_idle_time_seconds is not None and idle_time_seconds) > self.options.max_idle_time_seconds:
            client_info.close_client()
            return True

        return False

    def remove_stale_sockets(self):
        """
        清除僵尸链接， 如果存在的链接过少则创建链接
        :return:
        """
        if self.options.max_idle_time_seconds is not None:
            with self.lock:
                while self.clients and (self.clients[-1].idle_time_seconds() > self.options.max_idle_time_seconds):
                    client_info = self.clients.pop()
                    client_info.close_client()
        while True:
            with self.lock:
                if (len(self.clients) + self.active_clients) >= self.options.min_pool_size:
                    break

            client_info = self.connect()
            with self.lock:
                self.clients.appendleft(client_info)

    def __del__(self):
        for client_info in self.clients:
            client_info.close_client(None)


__Thrift_Pools = {}


def register_thrift_pool(name, service, host=None, port=None, timeout=8000, replace=True):
    """
    @params timeout: 客户端链接空闲超时：默认为8s，建议小于服务端空闲超时时间（默认10s）
    """
    global __Thrift_Pools
    if name not in __Thrift_Pools or replace:
        if not host:
            host = "127.0.0.1"
        if not port:
            port = 5000
        __Thrift_Pools[name] = Pool(host, port, service=service)


def get_thrift_pool(name):
    return __Thrift_Pools.get(name)


def clear_all_pools():
    for pool in __Thrift_Pools.values():
        pool.reset()
