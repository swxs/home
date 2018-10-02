import json
from enum import IntEnum
import requests
from common.AsyncFunction.aiohttp import aio_post
from common.Exceptions.UrlConvertFailedException import UrlConvertFailedException


class URL_CONVERT(IntEnum):
    LONG_TO_SHORT = 1
    SHORT_TO_LONG = 2


async def aio_convert_short_url(url):
    serviceurl = "http://dwz.cn/admin/create"
    data = {"url": url}
    body = json.dumps(data)
    response = await aio_post(serviceurl, body=body)
    result = json.loads(response.body)
    if result["Code"] != 0:
        raise UrlConvertFailedException(URL_CONVERT.LONG_TO_SHORT, result["Code"], result["LongUrl"], result["ShortUrl"], result["ErrMsg"])
    return result["ShortUrl"]


def convert_short_url(url):
    serviceurl = "http://dwz.cn/admin/create"
    data = {"url": url}
    body = json.dumps(data)
    response = requests.post(serviceurl, data=body)
    result = response.json()
    if result["Code"] != 0:
        raise UrlConvertFailedException(URL_CONVERT.LONG_TO_SHORT, result["Code"], result["LongUrl"], result["ShortUrl"], result["ErrMsg"])
    return result["ShortUrl"]


async def query_origin_url(shorturl):
    serviceurl = "http://dwz.cn/admin/query"
    data = {"shortUrl": shorturl}
    body = json.dumps(data)
    response = await aio_post(serviceurl, body=body)
    result = json.loads(response.body)
    if result["Code"] != 0:
        raise UrlConvertFailedException(URL_CONVERT.SHORT_TO_LONG, result["Code"], result["LongUrl"], result["shortUrl"], result["ErrMsg"])
    return result["LongUrl"]
