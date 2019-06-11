# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.Container import Container as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Container(BaseDAO):
    name = model.StringField()
    show_name = model.BooleanField()

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)

    @classmethod
    def get_container_by_container_id(cls, container_id):
        return cls.select(id=container_id)

