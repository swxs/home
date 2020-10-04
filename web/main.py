# -*- coding: utf-8 -*-

from logging import getLogger
import os
import sys
import logging
import tornado.ioloop
import tornado.locale
import tornado.escape
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets

import settings
from . import IBApplication

logger = logging.getLogger("main.web")


def main(port):
    tornado.locale.load_translations(settings.settings.get('translations'))
    application = IBApplication(**settings.settings).register_handlers(os.path.join(settings.SITE_ROOT))
    sockets = bind_sockets(port)
    server = HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)
    logger.debug('Tornado server started on port %s.' % port)
    tornado.ioloop.IOLoop.instance().start()
    logger.debug('Tornado server finished on port %s.' % port)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = settings.SITE_PORT

    main(port)
