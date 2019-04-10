# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.DatasourceUpload import *
from .Datasource import Datasource
from mongoengine_utils import NAME_DICT


class DatasourceUpload(Datasource):
    filename = model.StringField(helper_text='文件名')

    meta = {
    }


NAME_DICT["DatasourceUpload"] = DatasourceUpload
