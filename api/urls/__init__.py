# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @AUTH    : swxs
# @Time    : 2018/8/17 10:04

import os
from tornado.web import url
from importlib import import_module
import settings
from api.views import views


def load_urls():
    url_list = []
    BASE_PATH = os.path.join(settings.SITE_ROOT, "api", "urls")
    for root, dirname_list, filename_list in os.walk(BASE_PATH):
        for filename in filename_list:
            if filename not in ["__init__.py"]:
                base_path, _ = os.path.splitext(os.path.join(root, filename))
                base_path_list = base_path.split(os.sep)
                if "__pycache__" in base_path_list or ".DS_Store" in base_path_list:
                    continue
                module_path = ".".join(base_path_list[base_path_list.index("api"):])
                module = import_module(module_path)
                if hasattr(module, 'url_mapping'):
                    url_list.extend(module.url_mapping)
    return url_list


def get_api_urls():
    url_mapping = [
        url(r"/api/login/", views.LoginHandler, name='login'),
        url(r"/api/logout/", views.LogoutHandler, name='logout'),
    ]
    url_mapping.extend(load_urls())
    return url_mapping
