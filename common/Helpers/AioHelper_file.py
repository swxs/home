# -*- coding: utf-8 -*-
# @File    : aiohelper_file.py
# @AUTH    : swxs
# @Time    : 2018/9/19 10:17

import json
import os
import asyncio
import random
import aiofiles
import math
from tornado import gen
from tornado.httpclient import AsyncHTTPClient


async def aio_save_file_from_network(url, filepath):
    try:
        response = await AsyncHTTPClient().fetch(url)
        if response.code != 200:
            return False

        async with aiofiles.open(filepath, 'wb') as fd:
            await fd.write(response.body)
        return True
    except:
        return False
