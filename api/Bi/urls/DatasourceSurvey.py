# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.DatasourceSurvey import DatasourceSurveyHandler

url_mapping = [
    url(r"/api/bi/datasource_survey/(?:([a-zA-Z0-9&%\.~-]+)/)?", DatasourceSurveyHandler),
]
