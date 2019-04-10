# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.DatasourceSurvey import *
from .Datasource import Datasource
from mongoengine_utils import NAME_DICT


class DatasourceSurvey(Datasource):
    survey_id = model.ObjectIdField(helper_text='问卷id')

    meta = {
        'indexes': [
            {
                'fields': ['survey_id'],
            },
        ],
    }


NAME_DICT["DatasourceSurvey"] = DatasourceSurvey
