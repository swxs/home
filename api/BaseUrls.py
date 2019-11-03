# -*- coding: utf-8 -*-
# @File    : BaseUrls.py
# @AUTH    : swxs
# @Time    : 2019/4/10 11:50

import os
import settings
from tornado.web import url
from importlib import import_module


def load_urls():
    url_list = []
    BASE_PATH = os.path.join(settings.SITE_ROOT, "api")
    for root, dirname_list, filename_list in os.walk(BASE_PATH):
        for filename in filename_list:
            if filename not in ["__init__.py"]:
                base_path, _ = os.path.splitext(os.path.join(root, filename))
                base_path_list = base_path.split(os.sep)
                if "__pycache__" in base_path_list or ".DS_Store" in base_path_list:
                    continue
                module_path = ".".join(base_path_list[base_path_list.index("api"):])
                try:
                    module = import_module(module_path)
                    if hasattr(module, 'url_mapping'):
                        url_list.extend(module.url_mapping)
                except Exception as e:
                    print(e)
    return url_list


def get_api_urls():
    url_mapping = [
    ]
    url_mapping.extend(load_urls())
    return url_mapping
