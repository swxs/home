# -*- coding: utf-8 -*-

import tornado.web
from tornado.web import url

import settings
import api.urls as api_urls

url_mapping = [
    (r"/(favicon\.ico)", tornado.web.StaticFileHandler,
     {"path": "%s/static" % settings.SITE_ROOT}),
]

url_mapping.extend(api_urls.url_mapping)

application = tornado.web.Application(url_mapping, **settings.settings)
