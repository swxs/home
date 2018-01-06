# -*- coding: utf-8 -*-

from tornado.web import url
import views as views
from api.user import urls as user_urls

def get_api_urls():
    url_mapping = [
        url(r"/api/", views.IndexHandler, name='index'),
    ]
    url_mapping.extend(user_urls.url_mapping)
    return url_mapping
