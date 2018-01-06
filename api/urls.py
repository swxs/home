# -*- coding: utf-8 -*-

from tornado.web import url
import views as views
from api.user import urls as user_urls
from api.tag import urls as tag_urls
from api.artical import urls as artical_urls

def get_api_urls():
    url_mapping = [
        url(r"/api/", views.IndexHandler, name='index'),
    ]
    url_mapping.extend(user_urls.url_mapping)
    url_mapping.extend(tag_urls.url_mapping)
    url_mapping.extend(artical_urls.url_mapping)
    return url_mapping
