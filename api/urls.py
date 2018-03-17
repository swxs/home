# -*- coding: utf-8 -*-

from tornado.web import url

import views as views
from api.artical import urls as artical_urls
from api.user import urls as user_urls
from api.tag import urls as tag_urls
from api.password_lock import urls as password_lock_urls


def get_api_urls():
    url_mapping = [
        url(r"/api/", views.IndexHandler, name='index'),
        url(r"/api/login/", views.LoginHandler, name='login'),
        url(r"/api/logout/", views.LogoutHandler, name='logout'),
    ]
    url_mapping.extend(user_urls.url_mapping)
    url_mapping.extend(tag_urls.url_mapping)
    url_mapping.extend(artical_urls.url_mapping)
    url_mapping.extend(password_lock_urls.url_mapping)
    return url_mapping
