# coding=utf8
import os
import sys
import asyncio
import errno
import time
import yaml
import signal
from functools import partial
from typing import Optional
from importlib import reload
from importlib import import_module
from thriftpy2.contrib.aio.protocol.binary import TAsyncBinaryProtocolFactory
from thriftpy2.contrib.aio.transport.buffered import TAsyncBufferedTransportFactory
from thriftpy2.contrib.aio.socket import TAsyncServerSocket
from thriftpy2.contrib.aio.processor import TAsyncProcessor, TApplicationException
from thriftpy2.server import TServer
from thriftpy2.transport import TTransportException
from tornado import options
from tornado.process import cpu_count, gen_log, _reseed_random
from tornado.util import errno_from_exception, ObjectDict

from rpc.dispatcher import BaseDispatcher
from .server import TAsyncServer


def find_services(thrift):
    services = set()
    thrifts = []
    for key, val in vars(thrift).items():
        if type(val) == type:
            for base in val.__bases__[::-1]:
                if hasattr(base, 'thrift_service'):
                    services.update(base.thrift_services)
            services.update(val.thrift_services)
            thrifts.append(val)
    return thrifts, services


def gen_dispatcher(module_name_list):
    thrifts_list = []
    dispatchers = []
    services_set = set()
    for module_name in module_name_list:
        module_dispatchers = []
        module = import_module(module_name)
        for key, val in vars(module).items():
            is_dispatcher = False
            try:
                is_dispatcher = issubclass(val, BaseDispatcher)
            except TypeError:
                pass
            if is_dispatcher:
                module_dispatchers.append(val)
            elif hasattr(val, '__thrift_meta__'):
                (thrifts, services) = find_services(val)
                thrifts_list.extend(thrifts)
                services_set.update(services)

        base_dispatchers = []
        for idx, d1 in enumerate(module_dispatchers, 1):
            for d2 in module_dispatchers[idx:]:
                if issubclass(d1, d2):
                    base_dispatchers.append(d2)
                elif issubclass(d2, d1):
                    base_dispatchers.append(d1)
        dispatchers.extend(list(set(module_dispatchers) - set(base_dispatchers)))

    Dispatcher = type('Dispatcher', tuple(dispatchers), {})
    Service = type('Service', tuple(thrifts_list), {'thrift_services': services_set})
    return Dispatcher, Service


def make_server(port=None, module_list=None):
    if port:
        server_socket = TAsyncServerSocket(host="0.0.0.0", port=port, client_timeout=None)
    else:
        raise ValueError("port must be provided.")
    try:
        import socket

        s = socket.socket()
        s.bind(('0.0.0.0', port))
        s.close()
    except OSError:
        gen_log.exception('port %s is in use' % port)
    server_socket.listen()

    rpc_server = TAsyncServer(
        None,
        server_socket,
        iprot_factory=TAsyncBinaryProtocolFactory(),
        itrans_factory=TAsyncBufferedTransportFactory(),
    )
    rpc_server.start()

    Dispatcher, Service = gen_dispatcher(module_list)
    rpc_server.processor = TAsyncProcessor(Service, Dispatcher())

    return rpc_server


def force_exit(server, sig):
    server.shutdown()
    sys.exit(-1)


def run(port=None, module_list=None):
    assert port
    assert module_list
    server = make_server(port=port, module_list=module_list)
    signal.signal(signal.SIGINT, partial(force_exit, server))
    server.serve()


if __name__ == '__main__':
    with open("./config.yaml", 'r') as fp:
        rpc_settings = ObjectDict(yaml.safe_load(fp))

    port = rpc_settings.port
    module_list = rpc_settings.module_list
    run(port, module_list)
