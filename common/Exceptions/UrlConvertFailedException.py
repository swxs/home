# -*- coding: utf-8 -*-
# @File    : UrlConvertFailedException.py
# @AUTH    : swxs
# @Time    : 2018/9/25 10:10

from common.consts import *
from common.Utils.log_utils import getLogger

log = getLogger("Exception.UrlConvertFailedException")


class UrlConvertFailedException(Exception):
    def __init__(self, convert_type=CONVERT_URL_LONG_TO_SHORT, code=0, long_url="", short_url="", msg=""):
        self.convert_type = convert_type
        self.code = code
        self.long_url = long_url
        self.short_url = short_url
        self.msg = msg
        log.error(self)

    def __str__(self):
        if self.convert_type == CONVERT_URL_LONG_TO_SHORT:
            base_url = self.long_url
            base_url_type = "long"
        elif self.convert_type == CONVERT_URL_SHORT_TO_LONG:
            base_url = self.short_url
            base_url_type = "short"
        else:
            base_url = ""
            base_url_type = "unknow"
        return f"{base_url_type} url [{base_url}] convert failed! With msg {self.msg}"

    def __repr__(self):
        if self.convert_type == CONVERT_URL_LONG_TO_SHORT:
            base_url = self.long_url
            base_url_type = "long"
        elif self.convert_type == CONVERT_URL_SHORT_TO_LONG:
            base_url = self.short_url
            base_url_type = "short"
        else:
            base_url = ""
            base_url_type = "unknow"
        return f"{base_url_type} url [{base_url}] convert failed! With msg {self.msg}"
