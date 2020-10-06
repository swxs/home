# -*- coding: utf-8 -*-

import os
import sys
import signal
import logging
from functools import partial
import tornado.ioloop
import tornado.locale
import tornado.escape
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets

import settings
from . import IBApplication

logger = logging.getLogger("main.web")


def run(port):
    tornado.locale.load_translations(settings.web.get('translations'))
    application = IBApplication(**settings.web).register(os.path.join(settings.SITE_ROOT))
    sockets = bind_sockets(port)
    server = HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)
    return server


def force_exit(server, sig):
    logger.debug('Tornado server stoped %s.sig' % sig)
    server.stop()


def main(port):
    server = run(port=port)
    signal.signal(signal.SIGINT, partial(force_exit, server))
    logger.debug('Tornado server started on port %s.' % port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        logger.exception('unknown!')
    logger.debug('Tornado server finished on port %s.' % port)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = settings.SITE_PORT

    main(port)
