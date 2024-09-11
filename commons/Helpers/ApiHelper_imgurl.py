import aiohttp

from web.exceptions.http_500_internal_server_error_exception import (
    Http500InternalServerErrorException,
)

DOMAIN = 'https://www.imgurl.org'
UPLOAD_URL = f'{DOMAIN}/api/v2/upload'


class ImgurlHelper:
    def __init__(self, uid, token):
        self.uid = uid
        self.token = token

    async def upload_image(self, buffer, filename):
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field('file', buffer, filename=filename)
            form_data.add_field('uid', self.uid)
            form_data.add_field('token', self.token)

            async with session.post(UPLOAD_URL, data=form_data) as response:
                if response.status != 200:
                    raise Http500InternalServerErrorException(
                        Http500InternalServerErrorException.HelperServerError,
                        "ImgurlHelper Error",
                    )
                data = await response.json()
                return data["data"]["url"]
