# -*- coding: utf-8 -*-
import functools


class utils():
    def __init__(self, object):
        self.object = object

    @classmethod
    def single_or_muliteple(self, method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            ''''''
            if self.object_type:
                kwargs.update(dict(object=self.object))
                return method(self, *args, **kwargs)
            else:
                pass

        return wrapper
