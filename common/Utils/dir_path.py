# -*- coding: utf-8 -*-
# @File    : dir_path.py
# @AUTH    : swxs
# @Time    : 2018/5/31 15:58

import os
import sys
import subprocess


def get_dir_path(path, *paths):
    dir_path = os.path.join(path, *paths)
    if not os.path.exists(dir_path):
        if "win" in sys.platform:
            subprocess.call('mkdir {dir_path}'.format(dir_path=dir_path), shell=True)
        else:
            subprocess.call('mkdir -p {dir_path}'.format(dir_path=dir_path), shell=True)
    return dir_path
