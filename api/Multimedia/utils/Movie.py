# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Movie.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine_utils as model
from ..models.Movie import Movie as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Movie(BaseUtils):
    title = model.StringField()
    year = model.StringField()
    summary = model.StringField()

    def __init__(self, **kwargs):
        super(Movie, self).__init__(**kwargs)
