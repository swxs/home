# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.DatasourceUpload import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class DatasourceUpload(BaseModelDocument):
    filename = model.StringField(helper_text='文件名')

    meta = {
        'indexes': [
        ]
    }

NAME_DICT["DatasourceUpload"] = DatasourceUpload
