# -*- coding: utf-8 -*-
# @File    : DHelper_mongo.py
# @AUTH    : swxs
# @Time    : 2018/7/16 10:02

import string
import datetime
from collections import defaultdict

import pymongo
import numpy as np
import settings

from api.bi.field import enum as field_enum

from common.DHelper.DHelper_base import DHelper_base
from common.df_exception import NoDataException
from common.exception import CommonException


class DHelper_mongo(DHelper_base):
    def __new__(cls, *args):
        singleton = cls.__dict__.get('__singleton__')
        if singleton is not None:
            return singleton
        cls.client = pymongo.MongoClient(settings.MONGODB_ADDRESS, settings.MONGODB_PORT)
        if settings.MONGODB_USERNAME and settings.MONGODB_PASSWORD:
            cls.client.the_database.authenticate(settings.MONGODB_USERNAME, settings.MONGODB_PASSWORD, source='admin')
        cls.db = cls.client[settings.MONGODB_DBNAME]
        cls.collection = cls.db.rspd_data
        cls.__singleton__ = singleton = object.__new__(cls)
        return singleton
    
    def __init__(self, survey_id=None, project_id=None):
        if survey_id is not None:
            super(DHelper_mongo, self).__init__(survey_id)
            self.survey_id = survey_id
            
            self.match = dict(survey_id=self.survey_id)
            self.project = dict(_id=0, survey_id=1)
            self.group = dict({"_id": "$survey_id"})
            self.drilldown = dict(survey_id=self.survey_id)
    
    def _do_filter(self):
        for filter in self._filter_list:
            if filter.dtype == field_enum.DTYPE_DATETIME:
                start_time, end_time = filter.value_list
                filter_dict = {}
                if start_time:
                    filter_dict.update({"$gt": start_time})
                if end_time:
                    filter_dict.update({"$lt": end_time})
                self.match.update({filter.column: filter_dict})
            else:
                self.match.update({filter.column: {"$in": [int(value) for value in filter.value_list]}})
    
    def _do_add_new_column(self):
        for new_column in self._new_column_list:
            if new_column.dtype == field_enum.DTYPE_DATETIME:
                if new_column.dategroup == field_enum.DATEGROUP_YEAR:
                    self.project.update({new_column.new_column: {"$dateToString": {"format": "%Y", "date": "${column}".format(column=new_column.column)}}})
                elif new_column.dategroup == field_enum.DATEGROUP_QUARTER:
                    raise NotImplementedError()
                    self.project.update({new_column.new_column: {"$dateToString": {"format": "%Y-%Q", "date": "${column}".format(column=new_column.column)}}})
                elif new_column.dategroup == field_enum.DATEGROUP_MONTH:
                    self.project.update({new_column.new_column: {"$dateToString": {"format": "%Y-%m", "date": "${column}".format(column=new_column.column)}}})
                elif new_column.dategroup == field_enum.DATEGROUP_WEEK:
                    self.project.update({new_column.new_column: {"$dateToString": {"format": "%Y/%U", "date": "${column}".format(column=new_column.column)}}})
                elif new_column.dategroup == field_enum.DATEGROUP_DAY:
                    self.project.update({new_column.new_column: {"$dateToString": {"format": "%Y-%m-%d", "date": "${column}".format(column=new_column.column)}}})
            elif new_column.dtype == field_enum.DTYPE_DATETIME_Y:
                self.project.update({new_column.new_column: {"$dateToString": {"format": "%Y", "date": "${column}".format(column=new_column.column)}}})
            elif new_column.dtype == field_enum.DTYPE_DATETIME_Q:
                raise NotImplementedError()
                self.project.update({new_column.new_column: {"$dateToString": {"format": "%Q", "date": "${column}".format(column=new_column.column)}}})
            elif new_column.dtype == field_enum.DTYPE_DATETIME_M:
                self.project.update({new_column.new_column: {"$dateToString": {"format": "%m", "date": "${column}".format(column=new_column.column)}}})
            elif new_column.dtype == field_enum.DTYPE_DATETIME_W:
                self.project.update({new_column.new_column: {"$dateToString": {"format": "%U", "date": "${column}".format(column=new_column.column)}}})
            elif new_column.dtype == field_enum.DTYPE_DATETIME_WD:
                self.project.update({new_column.new_column: {"$dateToString": {"format": "%w", "date": "${column}".format(column=new_column.column)}}})
            elif new_column.dtype == field_enum.DTYPE_DATETIME_D:
                self.project.update({new_column.new_column: {"$dateToString": {"format": "%d", "date": "${column}".format(column=new_column.column)}}})
            else:
                self.project.update({new_column.new_column: "${column}".format(column=new_column.column)})
    
    def _do_drilldown(self):
        for drilldown in self._drilldown_list:
            self.drilldown.update({drilldown.new_column: drilldown.value})
    
    def do_preprocess(self):
        self._do_filter()
        self._do_add_new_column()
        self._do_drilldown()
    
    def get_aggfunc(self, pivot):
        if pivot.func == field_enum.AGGFUNC_MEAN:
            return {pivot.new_column: {"$avg": pivot.new_column}}
        elif pivot.func == field_enum.AGGFUNC_COUNT:
            return {pivot.new_column: {"$sum": 1}}
        return {}
    
    def do_pivot(self, has_colortag, fillna="-", change_func=None):
        SET_INDEX = False
        for pivot in self._pivot_main_list:
            if not pivot.aggable:
                raise CommonException("NOT IMPLIMENTED NOW!")
            
            if not SET_INDEX:
                group_dict = {}
                for index in pivot.index_list:
                    group_dict.update({index: "${index}".format(index=index)})
                self.group.update({"_id": group_dict})
                SET_INDEX = True
            self.group.update(self.get_aggfunc(pivot))
        aggregate_agg = [{"$match": self.match}, {"$project": self.project}, {"$match": self.drilldown}, {"$group": self.group}, {"$sort": {"_id": 1}}]
        self.result = DHelper_mongo.collection.aggregate(aggregate_agg)
    
    def do_rank(self, dtype, ascending, sortIndex, xAxisCount=None):
        pass
    
    def do_refresh(self, field_id_list):
        pass
    
    def get_pivot_data_result(self, start=0, end=None):
        '''
        'head': {'name': ['5a56c77bfdcf23104cffacdb'], 'value': [1L, 2L, 3L]}
        'data': [{'name': '5a4c3a5cfdcf231d104db135', 'value': [98159, 225832, 8632]}]
        'info': {'length': 1}
        '''
        head_name = []
        head_value = []
        _tmp_data = defaultdict(list)

        IS_FIRST_TURN = True
        for result in self.result:
            index_value = result['_id']
            if IS_FIRST_TURN:
                head_name = index_value.keys()
            value = index_value.values()
            if len(value) == 1:
                head_value.append(value[0])
            else:
                head_value.append(value)

            for key, value in result.items():
                if key != '_id':
                    _tmp_data[key].append(value)
            IS_FIRST_TURN = False
        data = [{"name": key, "value": value} for key, value in _tmp_data.items()]
        result_data = {"head": {"name": head_name, "value": head_value}, "data": data, "info": {"length": len(data)}}
        return result_data
    
    def get_pivot_data_as_raw_data_result(self, start=0, end=None):
        head_name = []
        head_value = []
        _tmp_data = defaultdict(list)
        
        IS_FIRST_TURN = True
        for index, result in enumerate(self.result):
            index_value = result['_id']
            if IS_FIRST_TURN:
                head_value.extend(index_value.keys())
            _tmp_data[index].extend(index_value.values())

            for key, value in result.items():
                if key != '_id':
                    if IS_FIRST_TURN:
                        head_value.append(key)
                    _tmp_data[index].append(value)
            IS_FIRST_TURN = False
        data = [{"name": key, "value": value} for key, value in _tmp_data.items()]
        result_data = {"head": {"name": head_name, "value": head_value}, "data": data, "info": {"length": len(data)}}
        return result_data
    
    def get_raw_data_result(self, index_list, start=0, end=None):
        pass
    
    def get_field_unique_value_list(self, column_name, dtype):
        return DHelper_mongo.collection.distinct(column_name)
    
    def get_base_data(self, start=0, end=None):
        # data = DHelper_mongo.collection.find({}).limit(50)
        return None
