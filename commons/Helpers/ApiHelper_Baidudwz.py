import json
import requests
import logging
from enum import IntEnum
from commons.Helpers import Helper_aiohttp

logger = logging.getLogger("ApiHelper_Baidudwz")


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


class Baidudwz_Helper:
    SHORT_TO_LONG_URL = "http://dwz.cn/admin/create"
    LONG_TO_SHORT_URL = "http://dwz.cn/admin/query"

    @classmethod
    async def aio_convert_short_url(cls, url):
        data = {"url": url}
        body = json.dumps(data)
        response = await Helper_aiohttp.post(cls.LONG_TO_SHORT_URL, body=body)
        result = json.loads(response.body)
        if result["Code"] != 0:
            raise UrlShortToLongConvertFailedException(
                code=result["Code"], message=result["ErrMsg"], url=url
            )
        return result["ShortUrl"]

    @classmethod
    async def aio_query_origin_url(cls, shorturl):
        data = {"shortUrl": shorturl}
        body = json.dumps(data)
        response = await Helper_aiohttp.post(cls.SHORT_TO_LONG_URL, body=body)
        result = json.loads(response.body)
        if result["Code"] != 0:
            raise UrlLongToShortConvertFailedException(
                code=result["Code"], message=result["ErrMsg"], url=shorturl
            )
        return result["LongUrl"]

    @classmethod
    def convert_short_url(cls, url):
        data = {"url": url}
        body = json.dumps(data)
        response = requests.post(cls.LONG_TO_SHORT_URL, data=body)
        result = response.json()
        if result["Code"] != 0:
            raise UrlShortToLongConvertFailedException(
                code=result["Code"], message=result["ErrMsg"], url=url
            )
        return result["ShortUrl"]

    @classmethod
    def query_origin_url(cls, shorturl):
        data = {"shorturl": shorturl}
        body = json.dumps(data)
        response = requests.post(cls.SHORT_TO_LONG_URL, data=body)
        result = response.json()
        if result["Code"] != 0:
            raise UrlLongToShortConvertFailedException(
                code=result["Code"], message=result["ErrMsg"], url=shorturl
            )
        return result["LongUrl"]
