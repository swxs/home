# -*- coding: utf-8 -*-
# @File    : ApiHelper_wjlink.py
# @AUTH    : swxs
# @Time    : 2019/8/23 9:46

import json
import requests
from enum import IntEnum
import settings
from urllib.parse import urlencode
from commons.AsyncFunction.aiohttp import aio_post
from commons import log_utils

logger = log_utils.get_logging('ApiHelper_wjlink')


class URL_CONVERT(IntEnum):
    LONG_TO_SHORT = 1
    SHORT_TO_LONG = 2


class UrlConvertFailedException(Exception):
    def __init__(self, code=0, message=""):
        self.code = code
        self.message = message
        self.url = ""
        self.base_url_type = "unknown"

    def __str__(self):
        return f"url [{self.url}] {self.base_url_type} convert failed! With msg {self.message}"

    def __repr__(self):
        return f"url [{self.url}] {self.base_url_type} convert failed! With msg {self.message}"


class UrlLongToShortConvertFailedException(UrlConvertFailedException):
    def __init__(self, code=0, message="", url=""):
        super(UrlLongToShortConvertFailedException, self).__init__(code, message)
        self.url = url
        self.base_url_type = "LongToShort"


class UrlShortToLongConvertFailedException(UrlConvertFailedException):
    def __init__(self, code=0, message="", url=""):
        super(UrlShortToLongConvertFailedException, self).__init__(code, message)
        self.url = url
        self.base_url_type = "ShortToLong"


async def aio_convert_short_url(url):
    data = {"url": url}
    body = urlencode(data)
    response = await aio_post(settings.WJLINK_SHORT_TO_LONG_URL, body=body)
    if not response.body:
        raise UrlLongToShortConvertFailedException(code=0, message="no result", url=url)
    result = json.loads(response.body)
    if result["code"] != 0:
        raise UrlLongToShortConvertFailedException(code=result["code"], message=result["msg"], url=url)
    return result["short_url"]


async def aio_query_origin_url(url):
    data = {"url": url}
    body = urlencode(data)
    response = await aio_post(settings.WJLINK_LONG_TO_SHORT_URL, body=body)
    if not response.body:
        raise UrlLongToShortConvertFailedException(code=0, message="no result", url=url)
    result = json.loads(response.body)
    if result["code"] != 0:
        raise UrlLongToShortConvertFailedException(code=result["code"], message=result["msg"], url=url)
    return result["long_url"]


def convert_short_url(url):
    data = {"url": url}
    response = requests.post(settings.WJLINK_SHORT_TO_LONG_URL, data=data)
    result = response.json()
    if result["code"] != 0:
        raise UrlLongToShortConvertFailedException(code=result["code"], message=result["msg"], url=url)
    return result["short_url"]


def query_origin_url(url):
    data = {"url": url}
    response = requests.post(settings.WJLINK_SHORT_TO_LONG_URL, data=data)
    result = response.json()
    if result["code"] != 0:
        raise UrlLongToShortConvertFailedException(code=result["code"], message=result["msg"], url=url)
    return result["long_url"]
