# -*- coding: utf-8 -*-
# @File    : create_chart.py
# @AUTH    : swxs
# @Time    : 2018/9/27 15:10

import os
import re
import json
import glob
import shutil
import asyncio
import datetime
import itertools
from bson import ObjectId
from functools import partial
from tornado.util import ObjectDict
from collections import defaultdict
from motorengine import BaseDocument, DocumentMetaclass
from motorengine.fields import ListField, DictField, ObjectIdField
from commons.Helpers.Helper_JsonEncoder import dump, load
from commons.Utils import df_utils

logger = log_utils.get_logging('helper_model_dump')


def _get_model_by_model_name(model_name):
    if isinstance(model_name, BaseDocument):
        return model_name
    elif isinstance(model_name, str):
        return model_dict[model_name]


def _get_model_name_by_name(model):
    if isinstance(model, BaseDocument):
        return getattr(model, "_class_name")
    elif isinstance(model, DocumentMetaclass):
        return getattr(model, "_class_name")
    elif isinstance(model, str):
        return model


class ModelCopyer(object):
    """
        连接一个mongodb，根据配置的规则深度遍历数据库，获取相关信息后， 提供导出到文件或另一个数据库的功能
    """
    def __init__(self):
        #  记录映射规则
        self._rules = dict()
        #  用来记录已生成的model的序号
        self.__copyed__ = dict()
        #  用来记录已生成对象的队列
        self.__itemdict__ = defaultdict(list)
        #  用来记录已生成model的数量
        self.__iteritem__ = defaultdict(itertools.count)
        #  用来记录生成对象的序号
        self.__objdict__ = defaultdict(list)

    def add_rule(self, source, target, field_name=None, change_func=None):
        """
        简介
        ----------
        添加关联规则：
        对于普通的关联关系数据，直接默认关联其创建序号
        对于需要特殊处理的关联关系数据， 通过传入的处理方法进行处理
        
        参数
        ----------
        source : 
            源数据表
        target : 
            关联数据表
        field_name [可选]: 默认为 None
            关联字段, 支持深度, 以(field, params)的格式传入
            对于普通字段，设置为 field
            对于简单的列表字段，设置为 field
            对于简单的字典字段，设置为 (field, key, ...) 支持多层
            对于键为可变对象的字典字段，设置为 (field, '__key')
                此时若其值亦为可变对象，设置为 (field, '__value', ...) 支持多层
        change_func [可选]: 默认为 None
            处理方法， 需要可以接收参数 obj(关联对象， 不存在是为None), obj_id(原始值)
        """
        if isinstance(field_name, (tuple, list)):
            if (source, field_name[0]) not in self._rules:
                self._rules[(source, field_name[0])] = defaultdict(dict)
            if change_func is None:
                self._rules[(source, field_name[0])][tuple(field_name[1:])] = target, None
            else:
                self._rules[(source, field_name[0])][tuple(field_name[1:])] = target, change_func
        else:
            if change_func is None:
                self._rules[(source, field_name)] = target, None
            else:
                self._rules[(source, field_name)] = target, change_func

    def __has_rule(self, model, field_name):
        return (_get_model_name_by_name(model), field_name) in self._rules

    def __get_rule(self, model, field_name):
        return self._rules[(_get_model_name_by_name(model), field_name)]

    def __get_key(self, model, obj_id):
        """
        简介
        ----------
        
        
        参数
        ----------
        model : 
            
        obj_id : 
            
        
        返回
        -------
        
        """
        return f"{_get_model_name_by_name(model)}: {obj_id}"

    def __has_copyed(self, model, obj_id):
        """
        简介
        ----------
        判断当前对象是否已被记录
        
        参数
        ----------
        model : 
            
        obj_id : 
            
        
        返回
        -------
        
        """
        return self.__get_key(model, obj_id) in self.__copyed__

    def __add_copyed(self, model, obj_id):
        """
        简介
        ----------
        将一个示例进行记录
        
        参数
        ----------
        model : 
            
        obj_id : 
            
        data : 
            
        
        返回
        -------
        
        """
        value = self.__copyed__[self.__get_key(model, obj_id)] = self.__iteritem__[_get_model_name_by_name(model)].__next__()
        self.__itemdict__[_get_model_name_by_name(model)].append({"t": _get_model_name_by_name(model), "v": value})
        return value

    def __update_copyed(self, model, index, data):
        self.__itemdict__[_get_model_name_by_name(model)][index]["d"] = data
        return index

    async def __read_deep_info(self, sub_model_group, value, stack=None):
        """
        简介
        ----------
        迭代读取深度信息， 作用于ListField或DictField类型
        
        参数
        ----------
        sub_model_group : 
            深层字段是形如: {param1: (target, change_func), param2: (target, change_func), ...}的字段
            非深层字段是形如: (target, change_func) 的元组
        value : 
            深层字段是可能包含属性的字典
            非深层字段是需要复制的属性
        stack [可选]: 默认为 None
            迭代记录
        
        返回
        -------
        
        """
        if stack is None:
            stack = []

        if isinstance(sub_model_group, dict):
            if isinstance(value, list):
                _new_value_list = list()
                for value_dict in value:
                    _new_value = dict()
                    for k, v in value_dict.items():
                        if tuple(stack + ["__key"]) in sub_model_group:
                            sub_sub_model_group, change_func = sub_model_group[tuple(stack + ["__key"])]
                            key = await self.read_info(sub_sub_model_group, k, change_func)

                            new_value_stack = stack + ["__value"]
                            if tuple(new_value_stack) in sub_model_group:
                                sub_sub_model_group, change_func = sub_model_group[tuple(new_value_stack)]
                                _new_value.update({key: await self.read_info(sub_sub_model_group, v, change_func)})
                            else:
                                _new_value.update({key: await self.__read_deep_info(sub_model_group, v, new_value_stack)})
                        else:
                            new_value_stack = stack + [k]
                            if tuple(new_value_stack) in sub_model_group:
                                sub_sub_model_group, change_func = sub_model_group[tuple(new_value_stack)]
                                _new_value.update({k: await self.read_info(sub_sub_model_group, v, change_func)})
                            else:
                                _new_value.update({k: await self.__read_deep_info(sub_model_group, v, new_value_stack)})
                    _new_value_list.append(_new_value)
                return _new_value_list
            elif isinstance(value, dict):
                _new_value = dict()
                for k, v in value.items():
                    if tuple(stack + ["__key"]) in sub_model_group:
                        sub_sub_model_group, change_func = sub_model_group[tuple(stack + ["__key"])]
                        key = await self.read_info(sub_sub_model_group, k, change_func)

                        new_value_stack = stack + ["__value"]
                        if tuple(new_value_stack) in sub_model_group:
                            sub_sub_model_group, change_func = sub_model_group[tuple(new_value_stack)]
                            _new_value.update({key: await self.read_info(sub_sub_model_group, v, change_func)})
                        else:
                            _new_value.update({key: await self.__read_deep_info(sub_model_group, v, new_value_stack)})
                    else:
                        new_value_stack = stack + [k]
                        if tuple(new_value_stack) in sub_model_group:
                            sub_sub_model_group, change_func = sub_model_group[tuple(new_value_stack)]
                            _new_value.update({key: await self.read_info(sub_sub_model_group, v, change_func)})
                        else:
                            _new_value.update({key: await self.__read_deep_info(sub_model_group, v, new_value_stack)})
                return _new_value
            else:
                return value
        else:
            # 处理非深层字段， 直接分list|dict进行处理
            if isinstance(value, list):
                sub_model_name, sub_model_change_func = sub_model_group
                return [await self.read_info(sub_model_name, val, sub_model_change_func) for val in value]
            elif isinstance(value, dict):
                _new_value = dict()
                for k, v in value.items():
                    if k in sub_model_group:
                        _new_value[k] = await self.read_info(sub_model_group[k][0], v, sub_model_group[key][1])
                    else:
                        _new_value[k] = v
                return _new_value
 
    async def read_info(self, model, obj_id, change_func=None):
        """
        简介
        ----------
        读取方法的入口
        
        参数
        ----------
        model : 
            需要处理的模块
        obj_id : 
            
        change_func [可选]: 默认为 None
            
        
        返回
        -------
        
        """
        if model is not None:
            model = _get_model_by_model_name(model)

        print(f"{_get_model_name_by_name(model)}: {obj_id}")
        if not self.__has_copyed(model, obj_id):
            try:
                if change_func is not None:
                    # 如果是通过转换方法获取的特殊数据， 则直接处理后返回
                    obj = await model.get_by_id(obj_id)
                    if obj is None:
                        logger.warning("copy_error id is None: obj_id: [%s], model: [%s]" % (obj_id, model))
                    return await change_func(obj, obj_id)
                else:
                    # 否则尝试获取到原始字段
                    obj = await model.get_by_id(obj_id)
                    if obj is None:
                        logger.error("copy_error id is None: obj_id: [%s], model: [%s]" % (obj_id, model))
                        return None
            except Exception as e:
                # print(obj_id, model)
                logger.exception("copy_error: obj_id: [%s], model: [%s]" % (obj_id, model))
                return None

            _index = self.__add_copyed(model, obj_id)
            data = dict()
            for field_name, field in obj.field_mappings.items():
                # 对不同类型的字段进行不同的处理
                if field_name == "oid":
                    continue
                value = obj.__getattribute__(field_name)
                if value is None:
                    continue

                if isinstance(field, ListField):
                    """
                    简介
                    ----------
                    对于ListField字段, 如果是关联字段，
                        深层字段是形如: {param1: (target, change_func), param2: (target, change_func), ...}的字典
                        非深层字段是形如: (target, change_func) 的元组
                    这边对于非深层字段， 直接取target
                    """
                    if self.__has_rule(model, field_name):
                        sub_model_name = self.__get_rule(model, field_name)
                        data[field_name] = await self.__read_deep_info(sub_model_name, value, [])
                    else:
                        data[field_name] = value
                elif isinstance(field, DictField):
                    if self.__has_rule(model, field_name):
                        sub_model_name = self.__get_rule(model, field_name)
                        data[field_name] = await self.__read_deep_info(sub_model_name, value, [])
                    else:
                        data[field_name] = value
                elif isinstance(field, ObjectIdField):
                    if self.__has_rule(model, field_name):
                        sub_model_name, change_func = self.__get_rule(model, field_name)
                        data[field_name] = await self.read_info(sub_model_name, value, change_func)
                    else:
                        data[field_name] = value
                else:
                    if self.__has_rule(model, field_name):
                        sub_model_name, change_func = self.__get_rule(model, field_name)
                        data[field_name] = await self.read_info(sub_model_name, value, change_func)
                    else:
                        data[field_name] = value
            return self.__update_copyed(model, _index, data)
        else:
            return self.__copyed__[self.__get_key(model, obj_id)]

    async def __write_deep_info(self, rule, value, stack=None):
        if stack is None:
            stack = []

        if isinstance(value, list):
            _new_value_list = list()
            for value_dict in value:
                _new_value = dict()
                for k, v in value_dict.items():
                    new_stack = stack + [k]
                    if tuple(new_stack) in rule:
                        _new_value.update({k: self.__objdict__[rule[tuple(new_stack)][0]][v]})
                    else:
                        _new_value.update({k: await self.__write_deep_info(rule, v, new_stack)})
                _new_value_list.append(_new_value)
            return _new_value_list
        elif isinstance(value, dict):
            _new_value = dict()
            for k, v in value.items():
                new_stack = stack + [k]
                if tuple(new_stack) in rule:
                    _new_value.update({k: self.__objdict__[rule[tuple(new_stack)][0]][v]})
                else:
                    _new_value.update({k: await self.__write_deep_info(rule, v, new_stack)})
            return _new_value
        else:
            return value

    async def write_info(self):
        for _model, _items in self.__itemdict__.items():
            for items in _items:
                model_name = items.get("t")
                self.__objdict__[model_name].append(ObjectId())

        for _model, _items in self.__itemdict__.items():
            for items in _items:
                model_name = items.get("t")
                model_data = items.get("d")
                model_index = items.get("v")

                model = _get_model_by_model_name(model_name)

                model_params = dict()
                model_params["id"] = self.__objdict__[model_name][model_index]
                for info_name, info_value in model_data.items():
                    field = getattr(model, "__mappings").get(info_name)
                    if isinstance(field, ListField):
                        if self.__has_rule(model, info_name):
                            rule = self._rules[(_get_model_name_by_name(model), info_name)]
                            if isinstance(rule, dict):
                                model_params[info_name] = await self.__write_deep_info(rule, info_value, [])
                            else:
                                model_params[info_name] = [self.__objdict__[rule[0]][info] for info in info_value]
                        else:
                            model_params[info_name] = info_value
                    elif isinstance(field, DictField):
                        if self.__has_rule(model, info_name):
                            rule = self._rules[(_get_model_name_by_name(model), info_name)]
                            if isinstance(rule, dict):
                                model_params[info_name] = await self.__write_deep_info(rule, info_value, [])
                        else:
                            model_params[info_name] = info_value
                    elif isinstance(field, ObjectIdField):
                        if self.__has_rule(model, info_name):
                            rule = self._rules[(_get_model_name_by_name(model), info_name)]
                            if isinstance(info_value, ObjectId):
                                model_params[info_name] = info_value
                            elif isinstance(info_value, str):
                                model_params[info_name] = ObjectId(info_value)
                            else:
                                # 这边是对应的顺序的那个对象的oid
                                if info_value is not None:
                                    model_params[info_name] = self.__objdict__[rule[0]][info_value]
                                else:
                                    # print(rule[0], info_value)
                                    logger.error("write_error: rule: [%s], info_value: [%s]" % (rule[0], info_value))
                        else:
                            model_params[info_name] = info_value
                    else:
                        if self.__has_rule(model, info_name):
                            rule = self._rules[(_get_model_name_by_name(model), info_name)]
                            if isinstance(info_value, ObjectId):
                                model_params[info_name] = str(info_value)
                            else:
                                # 这边是对应的顺序的那个对象的id
                                if info_value is not None:
                                    model_params[info_name] = str(self.__objdict__[rule[0]][info_value])
                                else:
                                    # print(rule[0], info_value)
                                    logger.error("write_error: rule: [%s], info_value: [%s]" % (rule[0], info_value))
                        else:
                            model_params[info_name] = info_value

                obj = model()
                for model_param_name, model_param in model_params.items():
                    setattr(obj, model_param_name, model_param)
                obj_id = await obj.save()
