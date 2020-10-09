# -*- coding: utf-8 -*-

import os
import sys
import signal
import logging
from functools import partial
from thriftpy2.contrib.aio.socket import TAsyncServerSocket

import settings
from . import TAsyncProcessor, TAsyncServer

logger = logging.getLogger("main.rpc")


def run(port):
    process = TAsyncProcessor.register(os.path.join(settings.SITE_ROOT))
    sockets = TAsyncServerSocket(host="0.0.0.0", port=port, client_timeout=None).listen()
    server = TAsyncServer(
        process,
        sockets,
    )
    return server


def force_exit(server, sig):
    logger.debug('thriftpy2 server stoped %s.sig' % sig)
    server.close()


def main(port):
    server = run(port=port)
    signal.signal(signal.SIGINT, partial(force_exit, server))
    logger.debug('thriftpy2 server started on port %s.' % port)
    server.serve()
    logger.debug('thriftpy2 server finished on port %s.' % port)
    sys.exit(0)


if __name__ == '__main__':
    import logging.config

    logging.config.fileConfig(os.path.join(settings.SITE_ROOT, 'logging.ini'))
    logger = logging.getLogger("main")

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = settings.SITE_PORT

    main()
