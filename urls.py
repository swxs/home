# -*- coding: utf-8 -*-

import tornado.web
import settings
import apps.BaseUrls as api_urls

url_mapping = [
    (r"/(favicon\.ico)", tornado.web.StaticFileHandler, {"path": "%s/static" % settings.SITE_ROOT}),
]

url_mapping.extend(api_urls.get_api_urls())

application = tornado.web.Application(url_mapping, **settings.settings)
