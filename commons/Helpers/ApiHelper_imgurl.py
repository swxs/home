import aiohttp

from web.exceptions.http_500_internal_server_error_exception import (
    Http500InternalServerErrorException,
)


class ImgurlHelper:
    def __init__(self, uid, token, domain):
        self.uid = uid
        self.token = token
        self.domain = domain

    async def upload_image(self, buffer, filename):
        api_url = f'{self.domain}/api/v2/upload'

        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field('file', buffer, filename=filename)
            form_data.add_field('uid', self.uid)
            form_data.add_field('token', self.token)

            async with session.post(api_url, data=form_data) as response:
                if response.status != 200:
                    raise Http500InternalServerErrorException(
                        Http500InternalServerErrorException.HelperServerError,
                        "ImgurlHelper Error",
                    )
                data = await response.json()
                return data["data"]["url"]
