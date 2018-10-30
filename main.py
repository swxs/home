# -*- coding: utf-8 -*-

import sys

import tornado.ioloop
import tornado.web
import tornado.locale
import tornado.escape
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets

import settings
import urls
from common.Utils.log_utils import getLogger

log = getLogger()

if len(sys.argv) > 1:
    MAIN_SITE_PORT = int(sys.argv[1])
else:
    MAIN_SITE_PORT = settings.SITE_PORT

if __name__ == "__main__":
    ''''''
    tornado.locale.load_translations(settings.settings.get('translations'))
    application = urls.application
    sockets = bind_sockets(MAIN_SITE_PORT)
    server = HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)
    log.debug('Tornado server started on port %s.' % MAIN_SITE_PORT)
    tornado.ioloop.IOLoop.instance().start()
