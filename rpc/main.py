# -*- coding: utf-8 -*-

import os
import sys
import signal
import logging
from functools import partial

from thriftpy2.contrib.aio.protocol.binary import TAsyncBinaryProtocolFactory
from thriftpy2.contrib.aio.transport.buffered import TAsyncBufferedTransportFactory
from thriftpy2.contrib.aio.socket import TAsyncServerSocket

import settings
from .server import TAsyncServer

logger = logging.getLogger("main.rpc")


def run(port):

    process = .register(module_list)
    sockets = TAsyncServerSocket(host="0.0.0.0", port=port, client_timeout=None).listen()
    
    server = TAsyncServer(
        process,
        sockets,
        iprot_factory=TAsyncBinaryProtocolFactory(),
        itrans_factory=TAsyncBufferedTransportFactory(),
    )
    server.start()
    logger.debug('thriftpy2 server started on port %s.' % port)
    server.serve()
    logger.debug('thriftpy2 server finished on port %s.' % port)


def force_exit(server, sig):
    server.shutdown()
    sys.exit(-1)


def main(port):
    server = run(port=port)
    signal.signal(signal.SIGINT, partial(force_exit, server))
    server


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = settings.SITE_PORT

    main()
