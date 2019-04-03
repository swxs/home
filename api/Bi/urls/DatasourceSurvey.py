# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.DatasourceSurvey import DatasourceSurveyHandler


url_mapping = [
    url(r"/api/DatasourceSurvey/(([a-zA-Z0-9&%\.~-]+)/)?", DatasourceSurveyHandler),
]
