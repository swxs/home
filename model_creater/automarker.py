# -*- coding: utf-8 -*-

import json
import os
import sys
import shutil
import textwrap
import copy
from functools import lru_cache
from collections import OrderedDict
from typing import *

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.curdir))

ALL_MODEL = [

]


def run():
    local_path = sys.path[0]
    abs_dir = os.path.dirname(local_path)
    base_path = os.path.join(abs_dir, "api", "auto")
    if os.path.isdir(base_path):
        shutil.rmtree(base_path)

    os.mkdir(base_path)

    for root, path, files in os.walk(os.path.join(os.getcwd(), "block")):
        for file in files:
            if not (ALL_MODEL is not None and file not in ALL_MODEL):
                marker = Marker(str(file))
                marker.save()


def _get_data_from_model_file(filename: str) -> Any:
    path = os.path.join(sys.path[0], "block", filename)
    with open(path, "r") as f:
        data = json.load(f)
        f.close()
    return data


class Marker:
    def __init__(self, model_setting_filename: str):
        self.info_dict = self._get_settings(model_setting_filename)
        self.model_name = self.info_dict.get("model_name", None)
        self.parent_name_list = self.info_dict.get("parent_name_list", [])
        self.model_enums_list = self.info_dict.get("model_enums_list", [])
        self.field_dict = self.info_dict.get("field_dict", {})
        self.info = self.info_dict.get('info', {})

        self.all_field_dict = self._get_all_field_dict()

        self.consts = ""
        self.models = ""
        self.utils = ""
        self.views = ""
        self.urls = ""
        self.docs = ""

    def save(self) -> None:
        if self.model_name:
            self.filename_list = [
                "consts.py",
                "models.py",
                "utils.py",
                "views.py",
                "urls.py",
                "docs.md"
            ]

            print("=" * 40)
            self.consts = self._init_consts()
            print(self.consts)

            print("-" * 40)
            self.models = self._init_models()
            print(self.models)

            print("-" * 40)
            self.utils = self._init_utils()
            print(self.utils)

            print("-" * 40)
            self.views = self._init_views()
            print(self.views)

            print("-" * 40)
            self.urls = self._init_urls()
            print(self.urls)

            print("-" * 40)
            self.docs = self._init_docs()
            print(self.docs)

            self._init_folder_and_file()

    def _get_settings(self, model_setting_filename: str) -> Dict[str, Any]:
        data = _get_data_from_model_file(model_setting_filename)

        name_list = data.get('name', None).split(".")
        if name_list[-1] == "":
            model_name = None
            parent_name_list = []
        else:
            model_name = name_list[-1]
            parent_name_list = name_list[0:-1]

        info = data.get('info', {})
        model_enums_list = data.get('enum', [])
        field_dict = {
            field.get('name'): field
            for field in data.get('settings', [])
            if field.get('name') is not None
        }
        return {
            "model_name": model_name,
            "parent_name_list": parent_name_list,
            "model_enums_list": model_enums_list,
            "field_dict": field_dict,
            "info": info
        }

    def _get_all_field_dict(self) -> Dict[str, Any]:
        info_dict_list = [self._get_settings(f"{name}.json") for name in self.parent_name_list]
        all_field_dict = copy.deepcopy(self.field_dict)
        [all_field_dict.update(info_dict.get('field_dict')) for info_dict in info_dict_list]
        return all_field_dict

    @lru_cache()
    def _get_title(self, name: str) -> str:
        """
        驼峰表示: field_name=>FieldName
        :param name: 
        :return: 
        """
        if "_" in name:
            str = ""
            name_part_list = name.split("_")
            for name_part in name_part_list:
                str += name_part.title()
            return str
        else:
            return name.title()

    @lru_cache()
    def _get_upper(self, name: str) -> str:
        """
        大写表示：field_name=>FIELDNAME
        :param name: 
        :return: 
        """
        if "_" in name:
            str = ""
            name_part_list = name.split("_")
            for name_part in name_part_list:
                str += name_part.upper()
            return str
        else:
            return name.upper()

    def _get_module_type(self, field: Dict[str, Any]) -> str:
        return field.get("type")

    def _get_editable_field_name_list(self, field_dict: Dict[str, Dict[str, Any]]) -> List[str]:
        return [
            field_name
            for field_name, field in field_dict.items()
            if field.get("settings", {}).get("editable", True)
        ]

    def _get_index_field_name_list(self, field_dict: Dict[str, Dict[str, Any]]) -> List[str]:
        return [
            field_name
            for field_name, field in field_dict.items()
            if field.get("settings", {}).get("indexes", False)
        ]

    def _get_list_type_field_name_list(self, field_dict: Dict[str, Dict[str, Any]]) -> List[str]:
        return [
            field_name
            for field_name, field in field_dict.items()
            if field.get("type") == "List"
        ]

    def _get_params(self, field: Dict[str, Any]) -> str:
        """
        设置字段model的参数列表
        :param field:
        :return:
        """
        return ", ".join(
            [
                "{0}={1}".format(key, value)
                for key, value in field.get('params', {}).items()
            ]
        )

    def _get_has_editable_selected(self, field_name_list: List[str]) -> str:
        return ", " if len(field_name_list) > 0 else ""

    def _concat_field_name_undefined_with_comma(self, field_name_list: List[str]) -> str:
        return ", ".join(f"{field_name}=undefined" for field_name in field_name_list)

    def _concat_field_selected_name_with_comma(self, field_name_list: List[str]) -> str:
        return ", ".join(f"{field_name}={field_name}" for field_name in field_name_list)

    def _concat_field_readable_name_with_comma(self, field_name_list: List[str]) -> str:
        return ", ".join(f"'{field_name}'" for field_name in field_name_list)

    def _concat_field_name_with_comma(self, field_name_list: List[str]) -> str:
        return ", ".join(field_name_list)

    def _init_folder_and_file(self):
        local_path = sys.path[0]
        abs_dir = os.path.dirname(local_path)

        self.abs_pathname = os.path.join(abs_dir, "api", "auto")
        if not os.path.isdir(self.abs_pathname):
            os.mkdir(self.abs_pathname)

        for filename in self.filename_list:
            file_name, file_type = os.path.splitext(filename)
            path = os.path.join(self.abs_pathname, file_name)
            if not os.path.isdir(path):
                os.mkdir(path)
            self._create_file(file_name, file_type)

    def _create_file(self, file_name, file_type):
        with open(os.path.join(self.abs_pathname, file_name, f"{self.model_name}{file_type}"), "w", encoding="utf8") as f:
            f.write(self.__dict__[file_name])
            f.close()

    def _init_enums_string(self):
        _str = ""
        if self.model_enums_list:
            for enum_setting in self.model_enums_list:
                enum_key = ""
                enum_key_value = ""
                for choice in enum_setting["choices"]:
                    choice_name = choice["name"]
                    choice_value = choice["value"]
                    choice_dispname = choice["disname"]
                    enum_key += """\
{choice_name} = {choice_value}
"""
                    enum_key_value += f"""\
    ({choice_name}, '{choice_dispname}'),
"""

                _str += f"""\
{enum_key}
{enum_setting["name"]} = [
{enum_key_value}
]
"""
        return _str

    def _init_consts(self):
        enum_content = self._init_enums_string()
        _str = f"""\
# -*- coding: utf-8 -*-

{enum_content}
"""
        return _str

    def _init_model_string(self):
        model_string = ""
        for field_name, field in self.field_dict.items():
            field_name = field.get('name')
            field_type = field.get('type')
            field_params = self._get_params(field)
            model_string += f"""\
    {field_name} = models.{field_type}Field({field_params})
"""
        return model_string

    def _init_model_index_string(self):
        _str = ""
        indexes_list = self._get_index_field_name_list(self.field_dict)
        if indexes_list:
            _str += f"""\
    meta = {{
        'indexes': [{indexes_list}]
    }}\
"""
        else:
            _str += ""
        return _str

    def _init_models(self):
        _str = f"""\
# -*- coding: utf-8 -*-

import datetime
import mongoengine as models
from common.Utils.log_utils import getLogger

log = getLogger("models/{self.model_name}")


class {self._get_title(self.model_name)}(models.Document):
{self._init_model_string()}
{self._init_model_index_string()}
"""
        return _str

    def _init_utils_string(self):
        utils_string = ""
        for field_name, field in self.field_dict.items():
            field_type = field.get('type')
            field_param = self._get_params(field)
            utils_string += f"""\
    {field_name} = models_fields.{field_type}Field({field_param})
"""
        return utils_string

    def _init_utils(self):
        _str = f"""\
# -*- coding: utf-8 -*-
        
import datetime
import models_fields
from BaseDocument import BaseDocument
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class {self._get_title(self.model_name)}(BaseDocument):
{self._init_utils_string()}
    def __init__(self, **kwargs):
        super({self._get_title(self.model_name)}, self).__init__(**kwargs)
"""
        return _str

    def _get_argument_type(self, field_name, list_field_list):
        return "get_argument" if field_name in list_field_list else "get_arguments"

    def _init_get_arguments(self, default=None):
        _str = ""
        for field_name in self._get_editable_field_name_list(self.all_field_dict):
            field = self.all_field_dict[field_name]
            field_name = field.get('name')
            argument_type = self._get_argument_type(field_name, self._get_list_type_field_name_list(self.all_field_dict))

            _str += f"""\
        {field_name} = self.{argument_type}('{field_name}', {default})
"""
        return _str

    def _init_views(self):
        model_name = self.model_name
        model_title = self._get_title(self.model_name)
        model_id = f"{model_name}_id"
        get_arguments = self._init_get_arguments(default="None")
        get_arguments_default = self._init_get_arguments(default="undefined")
        editable_selected_params = self._concat_field_selected_name_with_comma(self._get_editable_field_name_list(self.all_field_dict))
        version = self.info.get('version', 1)

        _str = f"""\
# -*- coding: utf-8 -*-

from base import BaseHandler
from api.consts.const import undefined
from api.utils.{model_name} import {model_title}
from common.Utils.log_utils import getLogger

log = getLogger("views/{model_name}")


class {model_title}Handler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, {model_id}=None):
        if {model_id}:
            {model_name} = {model_title}.select(id={model_id})
            return {model_name}.to_front()
        else:
            {model_name}_list = {model_title}.filter()
            return [{model_name}.to_front() for {model_name} in {model_name}_list]
    
    @BaseHandler.ajax_base()
    def post(self):
{get_arguments}
        {model_name} = {model_title}.create({editable_selected_params})
        return {model_name}.to_front()

    @BaseHandler.ajax_base()
    def put(self, {model_id}):
{get_arguments}
        {model_name} = {model_title}.select(id={model_id})
        {model_name} = {model_name}.update({editable_selected_params})
        return {model_name}.to_front()

    @BaseHandler.ajax_base()
    def patch(self, {model_id}):
{get_arguments_default}
        {model_name} = {model_title}.select(id={model_id})
        {model_name} = {model_name}.update({editable_selected_params})
        return {model_name}.to_front()

    @BaseHandler.ajax_base()
    def delete(self, {model_id}):
        {model_name} = {model_title}.select(id={model_id})
        {model_name}.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "{version}")
"""
        return _str

    def _init_urls(self):
        model_name = self.model_name
        model_title = self._get_title(self.model_name)

        _str = f"""\
# -*- coding: utf-8 -*-

from tornado.web import url
import api.views.{model_name} as views

url_mapping = [
    url(r"/api/{model_name}/create/", views.{model_title}Handler),
    url(r"/api/{model_name}/list/", views.{model_title}Handler),
    url(r"/api/{model_name}/select/([a-zA-Z0-9&%\.~-]+)/", views.{model_title}Handler),
    url(r"/api/{model_name}/update/([a-zA-Z0-9&%\.~-]+)/", views.{model_title}Handler),
    url(r"/api/{model_name}/delete/([a-zA-Z0-9&%\.~-]+)/", views.{model_title}Handler),
]
"""
        return _str

    def _init_info_dict(self):
        _str = ""
        for field_name in self._get_editable_field_name_list(self.all_field_dict):
            field = self.all_field_dict[field_name]
            field_name = field.get('name')
            field_type = field.get('type')

            _str += f"""\
|{field_name}|{field_type}||
"""
        return _str

    def _init_docs(self):
        model_name = self.model_name
        model_title = self._get_title(self.model_name)
        info_dict = self._init_info_dict()

        _str = f"""\
***

### **简要描述：**

创建{model_name}

### **请求URL：**

`/api/{model_name}/create/`

### **请求方式：**

POST

### **类型：**

### **请求参数：**

|参数名|参数类型|备注|
|:--|:--|:--|
{info_dict}

***

### **简要描述：**

更新{model_name}

### **请求URL：**

`/api/{model_name}/update/<{model_name}_id>`

### **请求方式：**

PATCH

### **类型：**

### **请求参数：**

|参数名|参数类型|备注|
|:--|:--|:--|
{info_dict}

***

### **简要描述：**

删除{model_name}

### **请求URL：**

`/api/{model_name}/delete/<{model_name}_id>`

### **请求方式：**

DELETE

### **类型：**

### **请求参数：**

|参数名|参数类型|备注|
|:--|:--|:--|

***

### **简要描述：**

获取{model_name}

### **请求URL：**

`/api/{model_name}/select/<{model_name}_id>`

### **请求方式：**

GET

### **类型：**

### **请求参数：**

|参数名|参数类型|备注|
|:--|:--|:--|
        """
        return _str


if __name__ == "__main__":
    """
    TODO LIST
    可能的优化内容
    1.√读取配置文件进行初始化， 可能的内容: 配置文件的设置， 配置文件的项目间复用， 配置文件的自动/可视化生成
    2.√完善parmas配置表， 实现从配置表获取对具体方法（CURD）的动态调整的可能
    3.√enum的统一配置， 对于部分基于其他表的enum如何动态同步, enum中的选项如何配置
    4.√添加has系列方法，辅助查询
    5. 待补充
    
    存在的难点与疑问
    1.√utils中， 涉及save()里的更新时间， 及refresh（）方法的相关内容处理
    2. 原本django中使用外键来进行的关系表处理， 在当前系统中如何实现
    3.√原本基于Exception的内部异常传递如何重构成适合当前系统
    4.√utils和bil的权责分配
    5. create 中的问题：
    1）√字段合法性检查
    2）√unique字段的是否重复
    3） 部分字段的自动默认取值, 
    6. get 中的问题：
    1） 多样化查询
    2） 联合查询如何自动处理
    3） 添加get_and_create方法, 实现对某些对象自动创建
    7. update 中的问题：
    1）√字段合法性检查
    2）√unique字段的是否重复
    3） 部分字段的自动修改, 如自增， 编辑时间等
    8. delete 中的问题：
    1） 删除是表示不可见还是彻底删除？ 正常不是错误数据不太会给予删除操作
    9.√patch方法添加， get_argument方法可能存在问题
    """
    run()
