import unittest
from types import SimpleNamespace

from home.web.exceptions import Http403ForbiddenException

from home.apps.upload.schemas.file_share_link import FileShareLinkCreate
from home.apps.upload.services.file_share_link_service import FileShareLinkService


USER_ID = "64f000000000000000000001"
OTHER_USER_ID = "64f000000000000000000002"
FILE_INFO_ID = "65f000000000000000000001"


class FakeFileInfoRepo:
    async def find_one(self, file_info_id):
        return SimpleNamespace(id=file_info_id, user_id=OTHER_USER_ID)


class FileShareLinkServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_user_cannot_share_another_users_file(self):
        service = FileShareLinkService(
            SimpleNamespace(),
            repo=SimpleNamespace(),
            file_info_repo=FakeFileInfoRepo(),
            upload_service=SimpleNamespace(),
        )
        schema = FileShareLinkCreate(
            file_info_id=FILE_INFO_ID,
            name="not mine",
        )

        with self.assertRaises(Http403ForbiddenException):
            await service.create(
                USER_ID,
                schema,
                SimpleNamespace(base_url="http://example.test/"),
            )


if __name__ == "__main__":
    unittest.main()
