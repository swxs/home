# -*- coding: utf-8 -*-

import os
import sys
import tornado.ioloop
import tornado.locale
import tornado.escape
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets

import settings
from web.web import IBApplication
from common.Utils.log_utils import getLogger

if __name__ == "__main__":
    ''''''
    log = getLogger()

    if len(sys.argv) > 1:
        MAIN_SITE_PORT = int(sys.argv[1])
    else:
        MAIN_SITE_PORT = settings.SITE_PORT
        
    tornado.locale.load_translations(settings.settings.get('translations'))
    application = IBApplication()
    application.register_handlers(os.path.join(settings.SITE_ROOT))
    sockets = bind_sockets(MAIN_SITE_PORT)
    server = HTTPServer(application, xheaders=True)
    server.add_sockets(sockets)
    log.debug('Tornado server started on port %s.' % MAIN_SITE_PORT)
    tornado.ioloop.IOLoop.instance().start()
    log.debug('Tornado server finished on port %s.' % MAIN_SITE_PORT)
