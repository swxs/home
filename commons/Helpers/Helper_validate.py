# -*- coding: utf-8 -*-

import re
import collections
try:
    from typing.re import Pattern
except Exception:
    Pattern = re.compile(r"")


class Validate(object):
    @classmethod
    def has(cls, value, reg):
        try:
            return re.search(rf'{reg}', value, flags=re.M) is not None
        except TypeError:
            return False

    @classmethod
    def any(cls, value, regs=None):
        try:
            if not isinstance(regs, collections.Iterable):
                return False
            return any(Validate.has(value, reg) for reg in regs)
        except TypeError:
            return False

    @classmethod
    def start_with(cls, value, reg):
        try:
            return re.match(rf'^{reg}', value, flags=re.M) is not None
        except TypeError:
            return False

    @classmethod
    def end_with(cls, value, reg):
        try:
            return re.match(rf'.*{reg}$', value, flags=re.M) is not None
        except TypeError:
            return False

    @classmethod
    def check(cls, value, reg):
        try:
            return re.match(rf'^{reg}$', value, flags=re.M) is not None
        except TypeError:
            return False

    @classmethod
    def clear(cls, value, reg):
        try:
            return re.sub(rf'{reg}', "", value, flags=re.M)
        except TypeError:
            return False

    @classmethod
    def get_all(cls, value, reg):
        try:
            result = re.findall(rf'({reg})+', value, flags=re.M)
            if len(result) > 0 and isinstance(result[0], tuple):
                return [value[0] for value in result]
            return result
        except TypeError:
            return []
