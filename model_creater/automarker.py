# -*- coding: utf-8 -*-
import json
import os
import sys
import shutil
import ConfigParser

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf8")


class Marker:
    def __init__(self, model_setting_filename):
        # todo 读取设置文件 初始化models_setting
        # self._get_setting()
        if self._get_setting_v2(model_setting_filename):
            self.filename_list = ["models", "enum", "urls", "utils", "views"]
            self.enum = self._init_enum()
            print(self.enum)
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

            self._init_folder_and_file()

    def _get_setting(self):
        self.model_name = "user"
        self.pathname = self.model_name
        self.model_setting_list = [
            {"name": "company_id", "type": "String", "parmas": {"max_length": "\"50\""},
             "setting": {"unique": False, "editable": False, "check": "all"}},
            {"name": "username", "type": "String", "parmas": {"max_length": "\"50\""},
             "setting": {"unique": True, "editable": True, "check": "all"}},
            {"name": "password", "type": "String", "parmas": {"max_length": "\"50\""},
             "setting": {"unique": False, "editable": True, "check": "password"}},
            {"name": "nickname", "type": "String", "parmas": {"max_length": "\"50\""},
             "setting": {"unique": False, "editable": True, "check": "all"}},
            {"name": "email", "type": "String", "parmas": {"max_length": "\"50\""},
             "setting": {"unique": True, "editable": True, "check": "email"}},
            {"name": "mobile", "type": "String", "parmas": {"max_length": "\"50\""},
             "setting": {"unique": False, "editable": True, "check": "mobile"}},
            {"name": "actived", "type": "Int", "parmas": {"default": "0"},
             "setting": {"unique": False, "editable": True, "check": "all"}},
            {"name": "status", "type": "Int", "parmas": {"default": "1"},
             "setting": {"unique": False, "editable": True, "check": "all"}},
            {"name": "role_list", "type": "List", "parmas": {"max_length": "\"50\""},
             "setting": {"unique": False, "editable": True, "check": "all"}},
            {"name": "created", "type": "DateTime", "parmas": {"default": "datetime.datetime.now"},
             "setting": {"unique": False, "editable": False, "check": "all"}},
            {"name": "updated", "type": "DateTime", "parmas": {"default": "datetime.datetime.now"},
             "setting": {"unique": False, "editable": False, "check": "all"}},
            {"name": "exp_time", "type": "DateTime", "parmas": {},
             "setting": {"unique": False, "editable": True, "check": "all"}},
            {"name": "description", "type": "String", "parmas": {"max_length": "\"50\""},
             "setting": {"unique": False, "editable": True, "check": "all"}}]
        self._init_parmas()

    def _get_setting_v2(self, model_setting_filename):
        path = os.path.join(sys.path[0], "block", model_setting_filename)
        with open(path, "r") as f:
            data = json.load(f)
            f.close()
        self.model_name = self.pathname = data.get('name', None)
        if self.model_name is None:
            return False
        self.model_title = self._get_title(self.model_name)
        self.model_upper = self._get_upper(self.model_name)
        self.model_setting_list = data.get('setting', [])
        self.model_enum_list = data.get('enum', [])
        self._init_parmas()
        return True

    def _get_title(self, name):
        if "_" in name:
            str = ""
            name_part_list = name.split("_")
            for name_part in name_part_list:
                str += name_part.title()
            return str
        else:
            return name.title()

    def _get_upper(self, name):
        if "_" in name:
            str = ""
            name_part_list = name.split("_")
            for name_part in name_part_list:
                str += name_part.upper()
            return str
        else:
            return name.upper()

    def _init_parmas(self):
        self.unique_parma_list = []
        self.edit_parma_list = []
        self.check_parma_dick = {}
        self.indexes_list = []
        for model_setting in self.model_setting_list:
            if model_setting.get('parms', {}).get('unique', False):
                self.unique_parma_list.append(model_setting.get('name', ''))
            if model_setting.get('settings', {}).get('editable', True):
                self.edit_parma_list.append(model_setting.get('name', ''))
            # if model_setting["setting"]["check"] and model_setting["setting"]["check"] != "all":
            #     self.check_parma_dick[model_setting["name"]] = model_setting["setting"]["check"]
            if model_setting.get('settings', {}).get('index', False):
                self.indexes_list.append("\"{0}\"".format(model_setting.get('name', '')))

        edit_select_parmas_list = []
        edit_selected_parmas_list = []
        for parma in self.edit_parma_list:
            edit_select_parmas_list.append("{0}=undefined".format(parma))
            edit_selected_parmas_list.append("{0}={0}".format(parma))

        unique_select_parmas_list = []
        unique_selected_parmas_list = []
        for parma in self.unique_parma_list:
            unique_select_parmas_list.append("{0}=undefined".format(parma))
            unique_selected_parmas_list.append("{0}={0}".format(parma))

        self.edit_select_parmas = ", ".join(edit_select_parmas_list)
        self.edit_selected_parmas = ", ".join(edit_selected_parmas_list)
        self.unique_select_parmas = ", ".join(unique_select_parmas_list)
        self.unique_selected_parmas = ", ".join(unique_selected_parmas_list)

        self.temp_unique_select = ", " if self.unique_select_parmas != "" else ""
        self.temp_edit_select = ", " if self.edit_select_parmas != "" else ""

    def _get_module_type(self, parma):
        for model_setting in self.model_setting_list:
            if model_setting.get('name') == parma:
                return model_setting.get("type")

    def _get_parmas(self, model_type, model_parmas):
        parmas_list = []
        if "required" in model_parmas:
            parmas_list.append("required={0}".format(model_parmas["required"]))
            # todo create里必须包含该字段的参数
        if "default" in model_parmas:
            parmas_list.append("default={0}".format(model_parmas["default"]))
            # todo create里默认为指定参数
        if "choices" in model_parmas:
            parmas_list.append("choices={0}".format(model_parmas["choices"]))
        if model_type == "String":
            if "max_length" in model_parmas:
                parmas_list.append("max_length={0}".format(model_parmas["max_length"]))
        elif model_type == "Int":
            pass
        elif model_type == "List":
            pass
        elif model_type == "DateTime":
            pass
        return ", ".join(parmas_list)

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

    def _init_enum_string(self):
        str = ""
        if self.model_enum_list:
            for enum_setting in self.model_enum_list:
                enum_key = ""
                enum_key_value = ""
                for choice in enum_setting["choices"]:
                    enum_key += """{0} = {1}
""".format(choice["name"], choice["value"])
                    enum_key_value += """   ({0}, u'{1}'),
""".format(choice["name"], choice["disname"])
                str += """
%(enum_key)s
%(enum_name)s = [
%(enum_key_value)s
]
    """ % {
                    "enum_key": enum_key,
                    "enum_name": enum_setting["name"],
                    "enum_key_value": enum_key_value
                }
        return str

    def _init_enum(self):
        str = """# -*- coding: utf-8 -*-"
%(enum_content)s
""" % {
            "enum_content": self._init_enum_string()
        }
        return str

    def _init_model_string(self):
        model_string = ""
        for model_setting in self.model_setting_list:
            model_string += """    
    %(name)s = models.%(model_type)sField(%(model_parmas)s)""" % {
                "name": model_setting["name"],
                "model_type": model_setting["type"],
                "model_parmas": self._get_parmas(model_setting["type"], model_setting["parmas"]),
            }
        return model_string

    def _init_model_index_string(self):
        print(self.indexes_list)
        if self.indexes_list != []:
            str = """
    meta = {
        'indexes': [%(indexes_list)s]
    }
""" % {
                "indexes_list": ", ".join(self.indexes_list)
            }
        else:
            str = ""
        return str

    def _init_models(self):
        str = """# -*- coding: utf-8 -*-
        
import json
import datetime
import enum as enum
import mongoengine as models
from tornado.util import ObjectDict
from basedoc import BaseDoc as BaseDoc


class %(model_title)s(models.Document, BaseDoc):%(model_content)s
%(model_indexes)s
""" % {
            "model_title": self.model_title,
            "model_content": self._init_model_string(),
            "model_indexes": self._init_model_index_string()
        }
        return str

    def _is_validate(self, parma_type):
        if parma_type in self.check_parma_dick:
            str = """
        if not Validate.check(%(parma_type)s, reg_type="%(check_type)s"):
            raise ValidateException(u"%(parma_type)s")""" % {
                "parma_type": parma_type,
                "check_type": self.check_parma_dick[parma_type]
            }
        else:
            str = ""
        return str

    def _is_create_unique(self, parma_type):
        if parma_type in self.unique_parma_list:
            print(parma_type, "_" * 40)
            str = """
        if get_%(model_name)s(%(parma_type)s=%(parma_type)s):
            raise MultException(u"%(parma_type)s")""" % {
                "model_name": self.model_name,
                "parma_type": parma_type
            }
        else:
            str = ""
        return str

    def _is_update_unique(self, parma_type):
        if parma_type in self.unique_parma_list:
            str = """
        if %(parma_type)s != %(model_name)s.%(parma_type)s and get_%(model_name)s(%(parma_type)s=%(parma_type)s):
            raise MultException(u"%(parma_type)s")""" % {
                "model_name": self.model_name,
                "parma_type": parma_type
            }
        else:
            str = ""
        return str

    def _init_util_select(self):
        str = ""
        for parma in self.unique_parma_list:
            str += """
        elif %(type)s != undefined:
            return get_%(model_name)s_by_%(type)s(%(type)s)""" % {
                "model_name": self.model_name,
                "type": parma
            }
        return str

    def _init_util_create(self):
        # [swxs] todo ask 这里的值传递感觉没什么意义了？
        str = ""
        for parma in self.edit_parma_list:
            str += """
    if %(type)s != undefined:
        %(model_name)s.%(type)s = %(type)s""" % {
                "model_name": self.model_name,
                "type": parma
            }
        return str

    def _init_util_update(self):
        str = ""
        for parma in self.edit_parma_list:
            str += """
    if %(type)s != undefined:
        %(model_name)s.%(type)s = %(type)s""" % {
                "model_name": self.model_name,
                "type": parma,
            }
        return str

    def _init_util_refresh(self):
        str = ""
        for parma in self.unique_parma_list:
            str += """
    get_%(model_name)s_by_%(type)s(%(model_name)s.%(type)s, refresh=1)""" % {
                "model_name": self.model_name,
                "type": parma,
            }
        return str

    def _init_util_refresh_list(self):
        str = ""
        for parma in self.unique_parma_list:
            str += """
@memorize
def get_%(model_name)s_by_%(type)s(%(type)s):
    try:
        return models.%(model_title)s.objects.get(%(type)s=%(type)s)
    except models.%(model_title)s.DoesNotExist:
        return None""" % {
                "model_name": self.model_name,
                "model_title": self.model_title,
                "type": parma,
            }
        return str

    def _init_utils(self):
        str = """# -*- coding: utf-8 -*-

from bson import ObjectId
from const import undefined
import models as models
from common.mem_cache import memorize
from common.validate import Validate
from common.exception import ValidateException, MultException

@memorize
def get_%(model_name)s_by_%(model_name)s_id(%(model_name)s_id):
    try:
        _id = ObjectId(%(model_name)s_id)
        return models.%(model_title)s.objects.get(id=_id)
    except models.%(model_title)s.DoesNotExist:
        return None

%(util_refresh_list)s

def get_%(model_name)s(%(model_name)s_id=undefined%(temp_unique_select)s%(unique_select_parmas)s):
    ''''''
    try:
        if %(model_name)s_id != undefined:
            return get_%(model_name)s_by_%(model_name)s_id(%(model_name)s_id)
        %(util_select)s
        else:
            return None
    except models.%(model_title)s.DoesNotExist:
        return None

def refresh_%(model_name)s(%(model_name)s):
    ''''''
    get_%(model_name)s_by_%(model_name)s_id(str(%(model_name)s.id), refresh=1)
    %(util_refresh)s
    
def create_%(model_name)s(%(edit_select_parmas)s):
    ''''''
    %(model_name)s = models.%(model_title)s()%(util_create)s
    %(model_name)s.save()
    refresh_%(model_name)s(%(model_name)s)
    return %(model_name)s

def has_%(model_name)s(%(model_name)s_id=undefined%(temp_unique_select)s%(unique_select_parmas)s):
    try:
        %(model_name)s = get_%(model_name)s(%(model_name)s_id=%(model_name)s_id%(temp_unique_select)s%(unique_selected_parmas)s)
        if %(model_name)s is None:
            return False 
        else:
            return True
    except models.%(model_title)s.DoesNotExist:
        return False

def update_%(model_name)s(%(model_name)s%(temp_edit_select)s%(edit_select_parmas)s):
    ''''''%(util_update)s
    %(model_name)s.save()
    refresh_%(model_name)s(%(model_name)s)
    return %(model_name)s

def delete_%(model_name)s(%(model_name)s):
    ''''''
    %(model_name)s.delete()
    refresh_%(model_name)s(%(model_name)s)
    
def to_front(%(model_name)s):
    ''''''
    return %(model_name)s.to_dict()
""" % {
            "model_name": self.model_name,
            "model_title": self.model_title,
            "temp_unique_select": self.temp_unique_select,
            "edit_select_parmas": self.edit_select_parmas,
            "unique_select_parmas": self.unique_select_parmas,
            "temp_edit_select": self.temp_edit_select,
            "unique_selected_parmas": self.unique_selected_parmas,
            "util_select": self._init_util_select(),
            "util_create": self._init_util_create(),
            "util_update": self._init_util_update(),
            "util_refresh": self._init_util_refresh(),
            "util_refresh_list": self._init_util_refresh_list(),
        }
        return str

    def _init_get_arguments(self):
        str = ""
        for parma in self.edit_parma_list:
            str += """
        %(type)s = self.%(get_argument)s('%(type)s', None)""" % {
                "get_argument": "get_argument" if self._get_module_type(parma) != "List" else "get_arguments",
                "type": parma
            }
        return str

    def _init_get_argument_default(self):
        str = ""
        for parma in self.edit_parma_list:
            str += """
        %(type)s = self.%(get_argument)s('%(type)s', undefined)""" % {
                "get_argument": "get_argument" if self._get_module_type(parma) != "List" else "get_arguments",
                "type": parma
            }
        return str

    def _init_views(self):
        str = """# -*- coding: utf-8 -*-

import cem_decorator
import enum as enum
import utils as utils
from base import BaseHandler
# from permission import enum as permission_enum
from const import undefined
from common.exception import ValidateException, MultException

class %(model_title)sHandler(BaseHandler):
    @BaseHandler.ajax_base
    # @cem_decorator.with_permission(permission_enum.PERM_%(model_upper)s_VIEW)
    def get(self, %(model_name)s_id=None):
        ''''''
        %(model_name)s = utils.get_%(model_name)s(%(model_name)s_id)
        return utils.to_front(%(model_name)s)
    
    @BaseHandler.ajax_base
    # @cem_decorator.with_permission(permission_enum.PERM_%(model_upper)s_EDIT)
    def post(self):
        %(get_arguments)s
        %(model_name)s = utils.create_%(model_name)s(%(edit_selected_parmas)s)
        return utils.to_front(%(model_name)s)
    
    @BaseHandler.ajax_base
    # @cem_decorator.with_permission(permission_enum.PERM_%(model_upper)s_EDIT)
    def put(self, %(model_name)s_id):
        %(get_arguments)s
        %(model_name)s = utils.get_%(model_name)s(%(model_name)s_id)
        %(model_name)s = utils.update_%(model_name)s(%(model_name)s%(temp_edit_select)s%(edit_selected_parmas)s)
        return utils.to_front(%(model_name)s)
    
    @BaseHandler.ajax_base
    # @cem_decorator.with_permission(permission_enum.PREM_%(model_upper)s_EDIT)
    def patch(self, %(model_name)s_id):
        %(get_argument_default)s
        %(model_name)s = utils.get_%(model_name)s(%(model_name)s_id)
        %(model_name)s = utils.update_%(model_name)s(%(model_name)s%(temp_edit_select)s%(edit_selected_parmas)s)
        return utils.to_front(%(model_name)s)
            
    @BaseHandler.ajax_base
    # @cem_decorator.with_permission(permission_enum.PERM_%(model_upper)s_EDIT)
    def delete(self, %(model_name)s_id):
        %(model_name)s = utils.get_%(model_name)s(%(model_name)s_id)
        utils.delete_%(model_name)s(%(model_name)s)
        return None
""" % {
            "model_name": self.model_name,
            "model_title": self.model_title,
            "model_upper": self.model_upper,
            "get_arguments": self._init_get_arguments(),
            "get_argument_default": self._init_get_argument_default(),
            "temp_edit_select": self.temp_edit_select,
            "edit_selected_parmas": self.edit_selected_parmas,
        }
        return str

    def _url_string(self):
        url_string = """url(r"/api/%(model_name)s/select/(\w+)/", views.%(model_title)sHandler, name='api_select_%(model_name)s'),
    url(r"/api/%(model_name)s/create/", views.%(model_title)sHandler, name='api_create_%(model_name)s'),
    url(r"/api/%(model_name)s/update/(\w+)/", views.%(model_title)sHandler, name='api_update_%(model_name)s'),
    url(r"/api/%(model_name)s/modify/(\w+)/", views.%(model_title)sHandler, name='api_modify_%(model_name)s'),
    url(r"/api/%(model_name)s/delete/(\w+)/", views.%(model_title)sHandler, name='api_delete_%(model_name)s'),
""" % {
            "model_name": self.model_name,
            "model_title": self.model_title
        }
        return url_string

    def _init_urls(self):
        str = """# -*- coding: utf-8 -*-

from tornado.web import url
import views as views

url_mapping = [
    %(url_content)s]
""" % {
            "url_content": self._url_string()
        }
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
            if file in ["tag.json"]:
                marker = Marker(str(file))
