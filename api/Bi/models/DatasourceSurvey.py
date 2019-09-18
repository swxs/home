# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.DatasourceSurvey import *
from .Datasource import Datasource
from settings import instance
from document_utils import NAME_DICT

@instance.register
class DatasourceSurvey(Datasource):
    survey_id = fields.ObjectIdField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['survey_id'],
            },
        ]
        pass


NAME_DICT["DatasourceSurvey"] = DatasourceSurvey
