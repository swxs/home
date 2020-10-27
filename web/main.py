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
    server = HTTPServer(application, xheaders=True)
    server.listen(port)
    loop = tornado.ioloop.IOLoop.instance()
    return loop


def force_exit(loop, signum, frame):
    logger.debug('Tornado server stoped %s.sig' % signum)
    loop.stop()


def main(port):
    loop = run(port=port)
    logger.debug('Tornado server started on port %s.' % port)
    signal.signal(signal.SIGINT, partial(force_exit, loop))
    try:
        loop.start()
    except Exception as e:
        logger.exception('unknown!')
    logger.debug('Tornado server finished on port %s.' % port)


if __name__ == "__main__":
    import logging.config

    logging.config.fileConfig(os.path.join(settings.SITE_ROOT, 'logging.ini'))
    logger = logging.getLogger("main")

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = settings.SITE_PORT

    signal.signal(signal.SIGINT, partial(print, "Ctrl + c"))
    main(port)
