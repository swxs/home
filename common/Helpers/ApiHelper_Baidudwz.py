from api.consts import *
import json
from enum import IntEnum
import requests
from common.AsyncFunction.aiohttp import aio_post
from common.Utils.log_utils import getLogger

log = getLogger("Exception.UrlConvertFailedException")


class URL_CONVERT(IntEnum):
    LONG_TO_SHORT = 1
    SHORT_TO_LONG = 2


class UrlConvertFailedException(Exception):
    def __init__(self, code=0, message=""):
        self.code = code
        self.message = message
        self.url = ""
        self.base_url_type = "unknow"

    def __str__(self):
        return f"url [{self.url}] {self.base_url_type} convert failed! With msg {self.message}"

    def __repr__(self):
        return f"url [{self.url}] {self.base_url_type} convert failed! With msg {self.message}"


class UrlLongToShortConvertFailedException(UrlConvertFailedException):
    def __init__(self, code=0, message="", url=""):
        super(UrlLongToShortConvertFailedException, self).__init__(code, message)
        self.url = url
        self.base_url_type = "LongToShort"
        log.error(self)


class UrlShortToLongConvertFailedException(UrlConvertFailedException):
    def __init__(self, code=0, message="", url=""):
        super(UrlShortToLongConvertFailedException, self).__init__(code, message)
        self.url = url
        self.base_url_type = "ShortToLong"
        log.error(self)


SHORT_TO_LONG_URL = "http://dwz.cn/admin/create"
LONG_TO_SHORT_URL = "http://dwz.cn/admin/query"


async def aio_convert_short_url(url):
    data = {"url": url}
    body = json.dumps(data)
    response = await aio_post(SHORT_TO_LONG_URL, body=body)
    result = json.loads(response.body)
    if result["Code"] != 0:
        raise UrlLongToShortConvertFailedException(code=result["Code"], message=result["ErrMsg"], url=result["LongUrl"])
    return result["ShortUrl"]


async def aio_query_origin_url(shorturl):
    data = {"shortUrl": shorturl}
    body = json.dumps(data)
    response = await aio_post(LONG_TO_SHORT_URL, body=body)
    result = json.loads(response.body)
    if result["Code"] != 0:
        raise UrlLongToShortConvertFailedException(code=result["Code"], message=result["ErrMsg"], url=result["shortUrl"])
    return result["LongUrl"]


def convert_short_url(url):
    data = {"url": url}
    body = json.dumps(data)
    response = requests.post(SHORT_TO_LONG_URL, data=body)
    result = response.json()
    if result["Code"] != 0:
        raise UrlLongToShortConvertFailedException(code=result["Code"], message=result["ErrMsg"], url=result["LongUrl"])
    return result["ShortUrl"]


def query_origin_url(shorturl):
    data = {"shorturl": shorturl}
    body = json.dumps(data)
    response = requests.post(LONG_TO_SHORT_URL, data=body)
    result = response.json()
    if result["Code"] != 0:
        raise UrlLongToShortConvertFailedException(code=result["Code"], message=result["ErrMsg"], url=result["shortUrl"])
    return result["LongUrl"]
