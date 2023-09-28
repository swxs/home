import io

import aiohttp

from web.exceptions.http_500_internal_server_error_exception import (
    Http500InternalServerErrorException,
)


class VVhanAsyncHelper:
    def __init__(self, domain):
        self.domain = domain
        self.cookie = None

    async def get_mving(self):
        # 调用获取列表的URL和参数
        api_url = f'{self.domain}/api/girl'

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    raise Http500InternalServerErrorException(
                        Http500InternalServerErrorException.HelperServerError,
                        "VVhanAsyncHelper Error",
                    )
                return io.BytesIO(await response.read())
