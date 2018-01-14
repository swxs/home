# -*- coding: utf-8 -*-
import json
import os
import sys
import shutil

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf8")


class Marker:
    def __init__(self, model_setting_filename):
        if self._get_setting(model_setting_filename):
            self.filename_list = ["models", "enums", "utils", "collections", "creater", "views", "urls"]
            self.models = self._init_models()
            print(self.models)

            print("-" * 40)
            self.enums = self._init_enums()
            print(self.enums)

            print("-" * 40)
            self.utils = self._init_utils()
            print(self.utils)

            print("-" * 40)
            self.collections = self._init_collections()
            print(self.collections)

            print("-" * 40)
            self.creater = self._init_creater()
            print(self.creater)

            print("-" * 40)
            self.views = self._init_views()
            print(self.views)

            print("-" * 40)
            self.urls = self._init_urls()
            print(self.urls)

            self._init_folder_and_file()

    def _get_setting(self, model_setting_filename):
        path = os.path.join(sys.path[0], "block", model_setting_filename)
        with open(path, "r") as f:
            data = json.load(f)
            f.close()

        self.model_name = self.pathname = data.get('name', None)
        if self.model_name is None:
            return False
        self.model_title = self._get_title(self.model_name)
        self.model_upper = self._get_upper(self.model_name)

        self.model_enums_list = data.get('enums', [])
        self.model_field_name_list = [field['name']
                                      for field in data.get('setting', [])
                                      if field.get('name') is not None]
        self.model_field_dict = {field.get('name'): field
                                 for field in data.get('setting', [])}

        self.unique_field_list = []
        self.required_field_list = []
        self.editable_field_list = []
        self.indexes_field_list = []
        for field_name in self.model_field_name_list:
            if self.model_field_dict[field_name]['parmas'].get('unique', False):
                self.unique_field_list.append(field_name)
            if self.model_field_dict[field_name]['parmas'].get('required', False):
                self.unique_field_list.append(field_name)
            if self.model_field_dict[field_name]['setting'].get('editable', True):
                self.editable_field_list.append(field_name)
            if self.model_field_dict[field_name]['setting'].get('indexes', True):
                self.indexes_field_list.append(field_name)
        if len(self.editable_field_list) > 0:
            self.has_editable_selected = ", "
        else:
            self.has_editable_selected = ""
        self.editable_select_parmas = ", ".join(
            ["{0}=undefined".format(field_name) for field_name in self.editable_field_list])
        self.editable_selected_parmas = ", ".join(
            ["{0}={0}".format(field_name) for field_name in self.editable_field_list])
        self.editable_attrs = ", ".join(["'{0}'".format(field_name) for field_name in self.editable_field_list])
        return True

    def _get_title(self, name):
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

    def _get_upper(self, name):
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

    def _get_module_type(self, field):
        return field.get("type")

    def _get_parmas(self, field):
        return ", ".join(["{0}={1}".format(key, value) for key, value in field.get('parmas', {}).iteritems()])

    def _init_folder_and_file(self):
        local_path = sys.path[0]
        abs_dir = os.path.dirname(local_path)

        self.abs_pathname = os.path.join(abs_dir, "api", "auto", self.pathname)
        if not os.path.isdir(self.abs_pathname):
            os.mkdir(self.abs_pathname)

            with open(os.path.join(self.abs_pathname, "__init__.py"), "w") as f:
                f.close()

            for filename in self.filename_list:
                self._create_file(filename)
        else:
            pass

    def _create_file(self, filename):
        with open(os.path.join(self.abs_pathname, "{0}.py".format(filename)), "w") as f:
            f.write(self.__dict__[filename])
            f.close()

    def _init_enums_string(self):
        str = ""
        if self.model_enums_list:
            for enum_setting in self.model_enums_list:
                enum_key = ""
                enum_key_value = ""
                for choice in enum_setting["choices"]:
                    enum_key += """{0} = {1}
""".format(choice["name"], choice["value"])
                    enum_key_value += """    ({0}, u'{1}'),
""".format(choice["name"], choice["disname"])

                str += """
{enum_key}
{enum_name} = [
{enum_key_value}
]
""".format(enum_key=enum_key,
           enum_name=enum_setting["name"],
           enum_key_value=enum_key_value)
        return str

    def _init_enums(self):
        str = """# -*- coding: utf-8 -*-"
class Enums():
    {enum_content}
    def __init__(self):
        pass
""".format(enum_content=self._init_enums_string())
        return str

    def _init_model_string(self):
        model_string = ""
        for field_name in self.model_field_name_list:
            model_string += """    
    {name} = models.{model_type}Field({model_parmas})""".format(
                name=self.model_field_dict[field_name].get('name'),
                model_type=self.model_field_dict[field_name].get('type'),
                model_parmas=self._get_parmas(self.model_field_dict[field_name]),
            )
        return model_string

    def _init_model_index_string(self):
        if self.indexes_field_list != []:
            str = """
    meta = {{
        'indexes': [{indexes_list}]
    }}
""".format(indexes_list=", ".join(["'{0}'".format(field_name) for field_name in self.indexes_field_list]))
        else:
            str = ""
        return str

    def _init_models(self):
        str = """# -*- coding: utf-8 -*-

import datetime
import mongoengine as models
from enums import Enums
from utils import Utils


class {model_title}(models.Document, Utils):{model_content}
{model_indexes}
    __attrs__ = [{model_attrs}]
    
    def __updateattr__(self, name, value):
        super({model_title}, self).__setattr__(name, value)

    def __unicode__(self):
        try:
            return self.oid
        except AttributeError:
            return self.oid

    @property
    def oid(self):
        return str(self.id)

    @property
    def creater(self):
        from creater import Creater
        return Creater()
""".format(model_title=self.model_title,
           model_content=self._init_model_string(),
           model_indexes=self._init_model_index_string(),
           model_attrs=self.editable_attrs)
        return str

    def _init_utils(self):
        str = """# -*- coding: utf-8 -*-

import datetime
from hashlib import md5
from mongoengine.errors import *
import settings
from const import undefined
from api.base_utils import BaseUtils
from common.Exceptions.ExistException import ExistException
from common.Exceptions.NotExistException import NotExistException
from common.Exceptions.ValidateException import ValidateException

class Utils(BaseUtils):
    def update_{model_name}(self, **kwargs):
        for attr in self.__attrs__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                self.__updateattr__(attr, value)
        self.updated = datetime.datetime.now()
        try:
            self.save()
        except NotUniqueError:
            raise ExistException("{model_title}")
        self.creater.refresh(self)
        return self

    def delete_{model_name}(self):
        self.delete()
        self.creater.refresh(self)
        return None

    def to_front(self):
        return self.to_dict()
""".format(model_name=self.model_name, model_title=self.model_title)
        return str

    def _init_collections(self):
        str = """# -*- coding: utf-8 -*-

class Collections():
    def __init__(self, {model_name}_list):
        self.{model_name}_list = {model_name}_list

    def to_front(self):
        return [{model_name}.to_front() for {model_name} in self.{model_name}_list]
""".format(model_name=self.model_name, model_title=self.model_title)
        return str

    def _init_creater(self):
        str = """# -*- coding: utf-8 -*-

from hashlib import md5
from bson import ObjectId
from mongoengine.errors import *
import settings
from const import undefined
from models import {model_title}
from collections import Collections
from common.Decorator.mem_cache import memorize
from common.Exceptions.ExistException import ExistException
from common.Exceptions.NotExistException import NotExistException


class Creater(object):
    def __new__(cls):
        singleton = cls.__dict__.get('__singleton__')
        if singleton is not None:
            return singleton
        cls.__singleton__ = singleton = object.__new__(cls)
        return singleton

    @classmethod
    def create_{model_name}(cls, **kwargs):
        {model_name} = {model_title}()
        for attr in {model_name}.__attrs__:
            value = kwargs.get(attr, undefined)
            if value != undefined:
                {model_name}.__updateattr__(attr, value)
        try:
            {model_name}.save()
        except NotUniqueError:
            raise ExistException("{model_title}")
        return {model_name}

    @classmethod
    def refresh(cls, {model_name}):
        cls.get_{model_name}_by_{model_name}_id({model_name}.oid, refresh=1)

    @classmethod
    @memorize
    def get_{model_name}_by_{model_name}_id(cls, {model_name}_id):
        try:
            _id = ObjectId({model_name}_id)
            return {model_title}.objects.get(id=_id)
        except {model_title}.DoesNotExist:
            raise NotExistException("{model_title}")

    @classmethod
    @memorize
    def has_{model_name}_by_{model_name}_id(cls, {model_name}_id):
        try:
            if Creater.get_{model_name}_by_{model_name}_id({model_name}_id):
                return True
            else:
                return False
        except NotExistException:
            return False

    @classmethod
    def get_{model_name}_list(cls):
        return Collections({model_title}.objects.all())
""".format(model_name=self.model_name, model_title=self.model_title)
        return str

    def _init_get_argumnet_type(self, field_name):
        return "get_argument" if self.model_field_dict[field_name].get('type') != "List" else "get_arguments"

    def _init_get_arguments(self, default=None):
        str = ""
        for field_name in self.editable_field_list:
            str += """
        {name} = self.{get_argument}('{name}', {default})""".format(
                default=default,
                get_argument=self._init_get_argumnet_type(field_name),
                name=self.model_field_dict[field_name].get('name'))
        return str

    def _init_views(self):
        str = """# -*- coding: utf-8 -*-

from const import undefined
from base import BaseHandler
from creater import Creater

class {model_title}Handler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, {model_name_id}=None):
        if {model_name_id}:
            {model_name} = Creater.get_{model_name}_by_{model_name_id}({model_name_id})
            return {model_name}.to_front()
        else:
            {model_name_list} = Creater.get_{model_name_list}()
            return {model_name_list}.to_front()

    @BaseHandler.ajax_base
    def post(self):{get_arguments}
        {model_name} = Creater.create_{model_name}({editable_selected_parmas})
        return {model_name}.to_front()
    
    @BaseHandler.ajax_base
    def put(self, {model_name_id}):{get_arguments}
        {model_name} = Creater.get_{model_name}_by_{model_name_id}({model_name_id})
        {model_name}.update_{model_name}({editable_selected_parmas})
        return {model_name}.to_front()

    @BaseHandler.ajax_base
    def patch(self, {model_name_id}):{get_arguments_default}
        {model_name} = Creater.get_{model_name}_by_{model_name_id}({model_name_id})
        {model_name}.update_{model_name}({editable_selected_parmas})
        return {model_name}.to_front()

    @BaseHandler.ajax_base
    def delete(self, {model_name_id}):
        {model_name} = Creater.get_{model_name}_by_{model_name_id}({model_name_id})
        {model_name}.delete_{model_name}()
        return None
""".format(model_name=self.model_name,
           model_name_id=self.model_name + "_id",
           model_name_list=self.model_name + "_list",
           model_title=self.model_title,
           model_upper=self.model_upper,
           get_arguments=self._init_get_arguments(default="None"),
           get_arguments_default=self._init_get_arguments(default="undefined"),
           has_editable_selected=self.has_editable_selected,
           editable_selected_parmas=self.editable_selected_parmas)
        return str

    def _url_string(self):
        url_string = """url(r"/api/{model_name}/(\w+)/", views.{model_title}Handler, name='api_select_{model_name}'),
    url(r"/api/{model_name}/", views.{model_title}Handler, name='api_select_{model_name}s'),
    url(r"/api/{model_name}/", views.{model_title}Handler, name='api_create_{model_name}'),
    url(r"/api/{model_name}/(\w+)/", views.{model_title}Handler, name='api_update_{model_name}'),
    url(r"/api/{model_name}/(\w+)/", views.{model_title}Handler, name='api_modify_{model_name}'),
    url(r"/api/{model_name}/(\w+)/", views.{model_title}Handler, name='api_delete_{model_name}'),
""".format(model_name=self.model_name, model_title=self.model_title)
        return url_string

    def _init_urls(self):
        str = """# -*- coding: utf-8 -*-

from tornado.web import url
import views as views

url_mapping = [
    {url_content}]
""".format(url_content=self._url_string())
        return str


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
    local_path = sys.path[0]
    abs_dir = os.path.dirname(local_path)
    base_path = os.path.join(abs_dir, "api", "auto")
    if os.path.isdir(base_path):
        shutil.rmtree(base_path)

    os.mkdir(base_path)

    for root, path, files in os.walk(os.path.join(os.getcwd(), "block")):
        for file in files:
            if file in ["password_lock.json"]:
            # if file:
                marker = Marker(str(file))
