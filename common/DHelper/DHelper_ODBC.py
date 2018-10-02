# -*- coding: utf-8 -*-
# @Author  : SWXS
# @File    : DHelper_ODBC.py
# @Time    : 2018/1/31 16:50

import string
import datetime
import numpy as np
from common.DBHelper_mysql import DBHelper


class DHelper_ODBC(object):
    def __new__(cls, *args):
        singleton = cls.__dict__.get('__singleton__')
        if singleton is not None:
            return singleton
        cls.__singleton__ = singleton = object.__new__(cls)
        return singleton
    
    def __init__(self, table_name=None, project_id=None):
        if table_name is not None:
            self._filter_list = []
            self._new_column_list = []
            self._field_filter_list = []
            self._drilldown_list = []
            self._pivot_main_list = []
            self._pivot_sub_list = []
            self.table_name = table_name
            self.sql = ""
    
    def add_filter(self, column_name, value_list, dtype):
        self._filter_list.append(dict(column_name=column_name,
                                      value_list=value_list,
                                      dtype=dtype))

    def add_new_column(self, new_column_name, column_name, aggable, dategroup, dtype, aggfunc_str, multifunc):
        self._new_column_list.append(dict(new_column_name=new_column_name,
                                          column_name=column_name,
                                          aggable=aggable,
                                          dategroup=dategroup,
                                          dtype=dtype,
                                          aggfunc_str=aggfunc_str,
                                          multifunc=multifunc))
    
    def add_drilldown(self, column_name, value):
        self._drilldown_list.append(dict(column_name=column_name,
                                         value=value))
    
    def add_field_filter(self, column_name, column, value_list):
        self._field_filter_list.append(dict(column_name=column_name,
                                            column=column,
                                            value_list=value_list))
    
    def add_main_pivot(self, column_name, index_list, func, multifunc):
        self._pivot_main_list.append(dict(column_name=column_name,
                                          index_list=index_list,
                                          func=func,
                                          multifunc=multifunc))
    
    def add_sub_pivot(self, column_name, index_list, func, multifunc):
        self._pivot_sub_list.append(dict(column_name=column_name,
                                         index_list=index_list,
                                         func=func,
                                         multifunc=multifunc))
    
    def do_preprocess(self):
        self.mapping = {}
        for new_column in self._new_column_list:
            self.mapping.update({new_column.get('new_column_name'): new_column.get('column_name')})
    
    def get_agg_name(self, func):
        if func == np.mean:
            return "AVG"
        elif func == len:
            return "COUNT"
        else:
            return "COUNT"
    
    def do_pivot(self, has_colortag, fillna="-", change_func=None):
        field_id_list = []
        for pivot in self._pivot_main_list:
            field_id_list.append("{AGG}({field_name}) as `v__{field_id}`".format(
                AGG=self.get_agg_name(pivot.get('func')),
                field_name=self.mapping.get(pivot.get('column_name')),
                field_id=pivot.get('column_name')
            ))
        if len(self._pivot_main_list) == 0:
            self.sql = ""
        else:
            index_field_list = self._pivot_main_list[0].get('index_list')
            if len(index_field_list) == 1:
                if index_field_list == ["All"]:
                    # field_id_list.append("All as `All`") #  等以后引入了预处理之后完善
                    GROUP = ""
                else:
                    field_id_list.append("{field_name} as `i__{field_id}`".format(
                        field_name="__".join([self.mapping.get(field_id) for field_id in index_field_list]),
                        field_id="__".join(index_field_list)
                    ))
                    GROUP = "GROUP BY {index_list}".format(index_list=", ".join([self.mapping.get(field_id) for field_id in index_field_list]))
            else:
                field_name = "CONCAT({0})"
                field_id_list.append("{field_name} as `i__{field_id}`".format(
                    field_name=field_name.format(", '__', ".join([self.mapping.get(field_id) for field_id in index_field_list])),
                    field_id="__".join(index_field_list)
                ))
                GROUP = "GROUP BY {index_list}".format(index_list=", ".join([self.mapping.get(field_id) for field_id in index_field_list]))
            
            self.sql = "SELECT {field_id_list} FROM {table_name} {GROUP};".format(
                field_id_list=", ".join(field_id_list),
                table_name=self.table_name,
                GROUP=GROUP
            )
        
        self.result_list = DBHelper().execute(self.sql)
    
    def do_rank(self, dtype, ascending, sortIndex, xAxisCount=None):
        pass
    
    def do_refresh(self, field_id_list):
        pass
    
    def get_pivot_data_result(self, start=0, end=None):
        head = dict()
        head["name"] = list()
        head["value"] = list()
        data_list = list()
        t = dict()
        if self.result_list:
            for result in self.result_list:
                for k, v in result.items():
                    if k not in t:
                        t[k] = list()
                    t[k].append(v)
        for k, v in t.items():
            field_info_list = k.split("__")
            if field_info_list[0] == "i":
                if len(field_info_list) == 2:
                    head["name"].append(field_info_list[1])
                    head["value"].extend(v)
                else:
                    head["name"].extend(field_info_list[1:])
                    for vv in v:
                        head["value"].append(vv.split("__"))
            elif field_info_list[0] == "v":
                field_data = dict()
                field_data["name"] = field_info_list[1]
                field_data["value"] = [int(x) for x in v]
                data_list.append(field_data)
        
        if len(head["name"]) == 0:
            #  等以后引入了预处理之后完善
            head["name"].append('All')
            head["value"].append('All')
        return dict(head=head, data=data_list)
    
    def get_pivot_data_as_raw_data_result(self, start=0, end=None):
        pass
    
    def get_raw_data_result(self, index_list, start=0, end=None):
        pass
    
    def get_field_unique_value_list(self, column_name, dtype):
        pass
    
    def get_base_data(self):
        return DBHelper(self.connect).execute(self.sql)
