# -*- coding: utf-8 -*-
# @File    : path_utils.py
# @AUTH    : swxs
# @Time    : 2018/5/31 15:58

import os


def get_dir_path(path, *paths):
    dir_path = os.path.join(path, *paths)
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except Exception as e:
            pass
    return dir_path


def get_signature(filename):
    return f"{os.path.getctime(filename)}_{os.path.getmtime(filename)}_{os.path.getsize(filename)}"
