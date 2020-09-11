# -*- coding: utf-8 -*-
# @File    : Helper_productor.py
# @AUTH    : swxs
# @Time    : 2019/6/27 16:37

import os
import sys
from fnmatch import fnmatch
from importlib import import_module


class NoModule(Exception):
    pass


class Productor(object):
    def __init__(self,
                 root_dir: str,
                 start_dir: str,
                 base_module: object,
                 temp_module: object,
                 pattern: str = '*.py'):
        """
        简介
        ----------


        参数
        ----------
        root_dir :
            系统根目录
        start_dir :
            查询根目录
        base_module :
            基础模块，所有查询对象应该是该类的子类
        temp_module :
            默认模块，设置为None时， 若没有查询到对象，会报NoModuleException
        pattern [可选]: 默认为 '*.py'
            文件匹配规则， 可以减小匹配范围加速匹配
        """
        # 所有加载模块的容器
        self.__productor = {}
        self.__path = {}

        self.base_module = base_module
        self.temp_module = temp_module
        self.root_dir = root_dir
        self.start_dir = start_dir
        self.pattern = pattern

    def __getitem__(self, item):
        if item not in self.__productor:
            self.discover()

        if item in self.__productor:
            return self.__productor[item]
        else:
            if self.temp_module:
                return self.temp_module
            else:
                raise ModuleNotFoundError(f"{item}不存在！")

    def __delitem__(self, item):
        del sys.modules[self.__path[item]]
        del self.__productor[item]
        del self.__path[item]

    def __contains__(self, item):
        return item in self.__productor

    def __match_path(self, path, full_path, pattern):
        # override this method to use alternative matching strategy
        return fnmatch(path, pattern)

    def __path_2_modulepath(self, path=''):
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

    def __load_module(self, module, module_path):
        try:
            name = getattr(module, "name")
        except Exception:
            name = getattr(module, "__name__")
        self.__productor[name] = module
        self.__path[name] = module_path

    def discover(self):
        start_dir = os.path.abspath(self.start_dir)

        if not os.path.isdir(start_dir):
            pass

        for root, dirs, files in os.walk(start_dir):
            for file_name in files:
                full_path = os.path.join(root, file_name)
                if self.__match_path(file_name, full_path, self.pattern):
                    try:
                        module_path = self.__path_2_modulepath(full_path)
                        module = import_module(module_path)
                        for name in dir(module):
                            obj = getattr(module, name)
                            if isinstance(obj, type) and issubclass(obj, self.base_module) and getattr(obj, "__module__") == module_path:
                                self.__load_module(obj, module_path)
                    except Exception as e:
                        print(full_path, e)
