# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model

import datetime
import mongoengine_utils as model
from ..models.DatasourceMerged import DatasourceMerged as _
from .Datasource import Datasource
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class DatasourceMerged(Datasource):
    datamerge_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(DatasourceMerged, self).__init__(**kwargs)

