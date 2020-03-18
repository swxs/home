# -*- coding: utf-8 -*-
# @File    : Organization.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Organization import OrganizationHandler

url_mapping = [
    url(r"/api/system/organization/(?:([a-zA-Z0-9&%\.~-]+)/)?", OrganizationHandler),
]
