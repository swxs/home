# encoding:utf-8
import os


def get_path_split(path):
    if not os.path.isdir(path):
        return None, None

    path = path.replace('\\', '/')
    if path.endswith('/'):
        path = path[:-1]
    return os.path.split(path)
