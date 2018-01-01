# -*- coding: utf-8 -*-

import json
from tornado.util import ObjectDict

class BaseDoc(object):
    @property
    def oid(self):
        return str(self.id)

    def to_dict(self):
        d = json.loads(self.to_json())
        d['id'] = self.oid
        d.pop('_id')
        return ObjectDict(d)

    def __unicode__(self):
        try:
            return self.name
        except AttributeError:
            return self.oid