# -*- coding: utf-8 -*-
# @File    : Helper_productor.py
# @AUTH    : swxs
# @Time    : 2019/6/27 16:37

import os
import sys
from fnmatch import fnmatch
from importlib import import_module


class Productor(object):
    def __init__(self, base_module, start_dir, pattern='*.py', top_level_dir=None, temp_module=None):
        self._productor = {}

        self.base_module = base_module
        self.temp_module = temp_module
        self.start_dir = start_dir
        self.pattern = pattern
        if top_level_dir is None:
            self.top_level_dir = self.start_dir
        else:
            self.top_level_dir = top_level_dir
        self.root_dir = os.path.dirname(os.path.abspath(__file__))

    def __getitem__(self, item):
        if item not in self._productor:
            self.discover()

        if item in self._productor:
            return self._productor[item]
        else:
            if self.temp_module:
                return self.temp_module
            return self.base_module

    def _path_2_modulepath(self, path=''):
        if path:
            path = path.replace('\\', '/').replace(self.root_dir.replace('\\', '/'), '')
            if path.startswith('/'):
                path = path[1:]
            path = path.replace('.py', '').replace('.PY', '')
            if set('.#~') & set(path):
                return None
            path = path.replace('/', '.').strip()
            if path:
                return path
        return None

    def _load_module(self, module):
        try:
            name = getattr(module, "__cname__")
        except Exception:
            name = getattr(module, "__class__")
        self._productor[name] = module

    def _match_path(self, path, full_path, pattern):
        # override this method to use alternative matching strategy
        return fnmatch(path, pattern)

    def discover(self):
        top_level_dir = os.path.abspath(self.top_level_dir)

        if os.path.isdir(os.path.abspath(top_level_dir)):
            for root, dirs, files in os.walk(top_level_dir):
                for file_name in files:
                    full_path = os.path.join(root, file_name)
                    if self._match_path(file_name, full_path, self.pattern):
                        try:
                            module_path = self._path_2_modulepath(full_path)
                            module = import_module(module_path)
                            for name in dir(module):
                                obj = getattr(module, name)
                                if isinstance(obj, type) and issubclass(obj, self.base_module) and getattr(obj, "__module__") == module_path:
                                    self._load_module(obj)
                        except Exception as e:
                            print(full_path, e)
        else:
            pass