import io

import aiohttp
from bs4 import BeautifulSoup

from web.exceptions.http_500_internal_server_error_exception import (
    Http500InternalServerErrorException,
)


class Million365AsyncHelper:
    def __init__(self, domain):
        self.domain = domain
        self.cookie = None

    async def get_mving(self):
        # 调用获取列表的URL和参数
        api_url = f'{self.domain}/api/?type=img&mode=3'

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    raise Http500InternalServerErrorException(
                        Http500InternalServerErrorException.HelperServerError,
                        "Million365AsyncHelper Error",
                    )
                result = await response.read()

            soup = BeautifulSoup(result)
            img = soup.img
            if img is None:
                raise Http500InternalServerErrorException(
                    Http500InternalServerErrorException.HelperServerError,
                    "Million365AsyncHelper Error",
                )

            async with session.get(img.attrs["src"]) as resp:
                return io.BytesIO(await resp.read())
