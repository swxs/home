# -*- coding: utf-8 -*-
# @File    : Helper_productor.py
# @AUTH    : swxs
# @Time    : 2019/6/27 16:37

import os
import sys
import logging
from fnmatch import fnmatch
from importlib import import_module
from typing import Dict, Generic, Optional, TypeVar, Union

logger = logging.getLogger("helper.Helper_productor")

T = TypeVar('T')


class NoModule(Exception):
    pass


class Productor(Generic[T]):
    def __init__(
        self,
        root_dir: str,
        start_dir: str,
        base_module: T,
        temp_module: Optional[T],
        pattern: str = '*.py',
    ):
        """
        简介
        ----------
        通过实例化Productor来初始化工厂(假设为productor), 通过productor[name]获取子类
            name为对应子类__name__

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
        self.__productor: Dict[Union[str, int], T] = {}
        self.__path: Dict[Union[str, int], str] = {}

        self.base_module = base_module
        if temp_module is None:
            self.temp_module = base_module
        else:
            self.temp_module = temp_module
        self.root_dir = root_dir
        self.start_dir = start_dir
        self.pattern = pattern

    def __getitem__(self, item: Union[str, int]) -> T:
        """
        简介
        ----------
        尝试获取匹配__name__的子类
        如果当前内存没有加载则去相应路径内查找匹配对应__name__的子类
        否则直接使用缓存的类

        参数
        ----------
        item :
        指定的__name__, 可以为数值或者字符串

        返回
        ----------
        对应子类

        异常
        ----------

        """
        if item not in self.__productor:
            self.discover()

        if item in self.__productor:
            return self.__productor[item]
        else:
            return self.temp_module

    def __delitem__(self, item: Union[str, int]) -> None:
        del sys.modules[self.__path[item]]
        del self.__productor[item]
        del self.__path[item]

    def __contains__(self, item: Union[str, int]) -> bool:
        return item in self.__productor

    def __match_path(self, path, full_path, pattern):
        # override this method to use alternative matching strategy
        return fnmatch(path, pattern)

    def __path_2_modulepath(self, path='') -> Optional[str]:
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

    def __load_module(self, module: T, module_path: str) -> None:
        try:
            name = getattr(module, "name")
        except Exception:
            name = getattr(module, "__name__")
        self.__productor[name] = module
        self.__path[name] = module_path

    def discover(self) -> None:
        start_dir = os.path.abspath(self.start_dir)

        if not os.path.isdir(start_dir):
            pass

        for root, dirs, files in os.walk(start_dir):
            for file_name in files:
                full_path = os.path.join(root, file_name)
                if self.__match_path(file_name, full_path, self.pattern):
                    try:
                        module_path = self.__path_2_modulepath(full_path)
                        if module_path is None:
                            continue
                        module = import_module(module_path)
                        for name in dir(module):
                            obj: T = getattr(module, name)
                            if (
                                isinstance(obj, type)
                                and issubclass(obj, self.base_module)
                                and getattr(obj, "__module__") == module_path
                            ):
                                self.__load_module(obj, module_path)
                    except Exception as e:
                        logger.warning(full_path, e)
