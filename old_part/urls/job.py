# -*- coding: utf-8 -*-

from tornado.web import url
import api.views.job as views

url_mapping = [
    url(r"/api/job/", views.JobHandler),
    url(r"/api/job/(\w+)/", views.JobHandler),
]
