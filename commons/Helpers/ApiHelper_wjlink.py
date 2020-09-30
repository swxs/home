# -*- coding: utf-8 -*-
# @File    : ApiHelper_wjlink.py
# @AUTH    : swxs
# @Time    : 2019/8/23 9:46

import json
import logging
import requests
from enum import IntEnum
from urllib.parse import urlencode
from . import Helper_aiohttp

logger = logging.get_logging('helper.ApiHelper_wjlink')


class UrlConvertFailedException(Exception):
    def __init__(self, code=0, message="", url=None, base_url_type=None):
        self.code = code
        self.message = message
        self.url = url
        self.base_url_type = base_url_type

    def __str__(self):
        return f"url [{self.url}] {self.base_url_type} convert failed! With msg {self.message}"

    def __repr__(self):
        return f"url [{self.url}] {self.base_url_type} convert failed! With msg {self.message}"


class UrlLongToShortConvertFailedException(UrlConvertFailedException):
    def __init__(self, code=0, message="", url=""):
        super(UrlLongToShortConvertFailedException, self).__init__(code, message, url, "LongToShort")


class UrlShortToLongConvertFailedException(UrlConvertFailedException):
    def __init__(self, code=0, message="", url=""):
        super(UrlShortToLongConvertFailedException, self).__init__(code, message, url, "ShortToLong")


class wjlink_Helper:
    LONG_TO_SHORT_URL = "http://wj.link/api/tinyurl/revert/"
    SHORT_TO_LONG_URL = "http://wj.link/api/tinyurl/shorten/"

    @classmethod
    async def aio_convert_short_url(cls, url):
        data = {"url": url}
        body = urlencode(data)
        response = await Helper_aiohttp.post(cls.LONG_TO_SHORT_URL, body=body)
        if not response.body:
            raise UrlLongToShortConvertFailedException(code=0, message="no result", url=url)
        result = json.loads(response.body)
        if result["code"] != 0:
            raise UrlLongToShortConvertFailedException(code=result["code"], message=result["msg"], url=url)
        return result["short_url"]

    @classmethod
    async def aio_query_origin_url(cls, url):
        data = {"url": url}
        body = urlencode(data)
        response = await Helper_aiohttp.post(cls.SHORT_TO_LONG_URL, body=body)
        if not response.body:
            raise UrlLongToShortConvertFailedException(code=0, message="no result", url=url)
        result = json.loads(response.body)
        if result["code"] != 0:
            raise UrlLongToShortConvertFailedException(code=result["code"], message=result["msg"], url=url)
        return result["long_url"]

    @classmethod
    def convert_short_url(cls, url):
        data = {"url": url}
        response = requests.post(cls.LONG_TO_SHORT_URL, data=data)
        result = response.json()
        if result["code"] != 0:
            raise UrlLongToShortConvertFailedException(code=result["code"], message=result["msg"], url=url)
        return result["short_url"]

    @classmethod
    def query_origin_url(cls, url):
        data = {"url": url}
        response = requests.post(cls.SHORT_TO_LONG_URL, data=data)
        result = response.json()
        if result["code"] != 0:
            raise UrlLongToShortConvertFailedException(code=result["code"], message=result["msg"], url=url)
        return result["long_url"]
