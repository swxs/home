# -*- coding: utf-8 -*-

import json
from tornado.util import ObjectDict

class BaseUtils(object):
    def to_dict(self):
        d = json.loads(self.to_json())
        d['id'] = self.oid
        d.pop('_id')
        return ObjectDict(d)
