# -*- coding: utf-8 -*-

import re
import collections

try:
    from typing.re import Pattern
except Exception:
    Pattern = re.compile(r"")


def has(value, reg):
    try:
        return re.search(rf'{reg}', value, flags=re.M) is not None
    except TypeError:
        return False


def has_any(value, regs=None):
    try:
        if not isinstance(regs, collections.Iterable):
            return False
        return any(has(value, reg) for reg in regs)
    except TypeError:
        return False


def start_with(value, reg):
    try:
        return re.match(rf'^{reg}', value, flags=re.M) is not None
    except TypeError:
        return False


def end_with(value, reg):
    try:
        return re.match(rf'.*{reg}$', value, flags=re.M) is not None
    except TypeError:
        return False


def check(value, reg):
    try:
        return re.match(rf'^{reg}$', value, flags=re.M) is not None
    except TypeError:
        return False


def clear(value, reg):
    try:
        return re.sub(rf'{reg}', "", value, flags=re.M)
    except TypeError:
        return False


def get_all(value, reg):
    try:
        result = re.findall(rf'({reg})+', value, flags=re.M)
        if len(result) > 0 and isinstance(result[0], tuple):
            return [value[0] for value in result]
        return result
    except TypeError:
        return []
