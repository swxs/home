# -*- coding: utf-8 -*-
# @File    : dir_path.py
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
