# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.DatasourceSurvey import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class DatasourceSurvey(BaseModelDocument):
    survey_id = model.ObjectIdField(helper_text='问卷id')

    meta = {
        'indexes': [
            {
                'fields': ['survey_id'],
            },
        ]
    }

NAME_DICT["DatasourceSurvey"] = DatasourceSurvey
