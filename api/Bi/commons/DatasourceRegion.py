# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.DatasourceRegion import DatasourceRegion as _
from .Datasource import Datasource
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class DatasourceRegion(Datasource):
    region_type_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(DatasourceRegion, self).__init__(**kwargs)

    @classmethod
    def get_datasource_region_by_datasource_region_id(cls, datasource_region_id):
        return cls.select(id=datasource_region_id)

