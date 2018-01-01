# -*- coding: utf-8 -*-
import functools


class utils():
    def __init__(self, object):
        self.object = object

    @classmethod
    def single_or_multiple(self, method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            ''''''
            if str(type(self.object)) == "<class 'mongoengine.queryset.queryset.QuerySet'>":
                def map(object):
                    kwargs.update(dict(object=object))
                    return method(self, *args, **kwargs)
                return [map(object) for object in self.object]
            else:
                kwargs.update(dict(object=self.object))
                return method(self, *args, **kwargs)
        return wrapper
