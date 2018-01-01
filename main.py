# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.escape
import sys
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets

import settings
import urls
from base import PageNotFoundHandler
from common.Utils.log_utils import getLogger

log = getLogger('main.py')

if len(sys.argv) > 1:
    MAIN_SITE_PORT = int(sys.argv[1])
else:
    MAIN_SITE_PORT = settings.SITE_PORT

tornado.web.ErrorHandler = PageNotFoundHandler

if __name__ == "__main__":
    ''''''
    tornado.locale.load_translations(settings.settings.get('translations'))
    application = urls.application
    sockets = bind_sockets(MAIN_SITE_PORT)
    server = HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)
    log.debug('Tornado server started on port %s.' % MAIN_SITE_PORT)
    tornado.ioloop.IOLoop.instance().start()
    print "start"
