# -*- coding: utf-8 -*-
# @File    : aiohttp.py
# @AUTH    : swxs
# @Time    : 2018/6/7 14:38

import json
import requests
from tornado.httpclient import AsyncHTTPClient
from common.ApiExceptions import *


async def aio_get(url, headers=None):
    if headers is None:
        headers = {}
    response = await AsyncHTTPClient().fetch(url, headers=headers)
    return response


async def aio_post(url, body="", headers=None):
    if headers is None:
        headers = {}
    response = await AsyncHTTPClient().fetch(url, method='POST', body=body, headers=headers)
    return response
