import io

import aiohttp

from web.exceptions.http_500_internal_server_error_exception import (
    Http500InternalServerErrorException,
)

DOMAIN = 'https://api.vvhan.com'
GET_MVING_URL = f'{DOMAIN}/api/girl'


class VVhanAsyncHelper:
    def __init__(self):
        self.cookie = None

    async def get_mving(self):
        # 调用获取列表的URL和参数
        async with aiohttp.ClientSession() as session:
            async with session.get(GET_MVING_URL) as response:
                if response.status != 200:
                    raise Http500InternalServerErrorException(
                        Http500InternalServerErrorException.HelperServerError,
                        "VVhanAsyncHelper Error",
                    )
                return io.BytesIO(await response.read())
