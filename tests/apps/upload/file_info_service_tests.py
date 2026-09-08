import unittest
from types import SimpleNamespace

from home.web.exceptions import Http403ForbiddenException
from home.web.schemas.pagination import PageSchema

from home.apps.upload.schemas.file_info import FileInfoFilter
from home.apps.upload.services.file_info_service import FileInfoService
from home.apps.upload.storage import build_object_key


USER_ID = "64f000000000000000000001"
OTHER_USER_ID = "64f000000000000000000002"
FILE_INFO_ID = "65f000000000000000000001"
MD5 = "d41d8cd98f00b204e9800998ecf8427e"


def record(user_id=USER_ID):
    return SimpleNamespace(
        id=FILE_INFO_ID,
        user_id=user_id,
        file_id=MD5,
        file_name="empty.txt",
        file_size=0,
        ext=".txt",
        policy=1,
    )


class FakeDB:
    async def commit(self):
        return None

    async def rollback(self):
        return None


class FakeRepo:
    def __init__(self, *, owned=None, references=0):
        self.owned = owned
        self.references = references
        self.deleted = []
        self.seen_filter = None

    async def search(self, schema, page_schema):
        self.seen_filter = schema
        data = [self.owned] if self.owned else []
        return {"data": data, "pagination": {"total": len(data)}}

    async def find_owned(self, file_info_id, user_id, *, for_update=False):
        if self.owned and self.owned.id == file_info_id and self.owned.user_id == user_id:
            return self.owned
        return None

    async def delete_one(self, file_info_id):
        self.deleted.append(file_info_id)
        return 1

    async def count_content_references(self, file_id, file_size):
        return self.references


class FakeShareRepo:
    def __init__(self):
        self.revoked = []

    async def revoke_active_for_file(self, file_info_id):
        self.revoked.append(file_info_id)
        return 1


class FakeOSS:
    def __init__(self):
        self.deleted = []

    def delete(self, key):
        self.deleted.append(key)


class FileInfoServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_list_forces_authenticated_user_filter(self):
        repo = FakeRepo(owned=record())
        service = FileInfoService(
            FakeDB(),
            repo=repo,
            share_repo=FakeShareRepo(),
            oss_helper=FakeOSS(),
        )

        result = await service.list(USER_ID, FileInfoFilter(), PageSchema())

        self.assertEqual(repo.seen_filter.user_id, USER_ID)
        self.assertEqual(len(result["data"]), 1)

    async def test_get_rejects_other_user(self):
        service = FileInfoService(
            FakeDB(),
            repo=FakeRepo(owned=record()),
            share_repo=FakeShareRepo(),
            oss_helper=FakeOSS(),
        )

        with self.assertRaises(Http403ForbiddenException):
            await service.get(OTHER_USER_ID, FILE_INFO_ID)

    async def test_last_reference_revokes_shares_and_deletes_object(self):
        repo = FakeRepo(owned=record(), references=0)
        shares = FakeShareRepo()
        oss = FakeOSS()
        service = FileInfoService(
            FakeDB(),
            repo=repo,
            share_repo=shares,
            oss_helper=oss,
        )

        count = await service.delete(USER_ID, FILE_INFO_ID)

        self.assertEqual(count, 1)
        self.assertEqual(shares.revoked, [FILE_INFO_ID])
        self.assertEqual(oss.deleted, [build_object_key(MD5, 0)])

    async def test_shared_content_is_retained(self):
        repo = FakeRepo(owned=record(), references=1)
        oss = FakeOSS()
        service = FileInfoService(
            FakeDB(),
            repo=repo,
            share_repo=FakeShareRepo(),
            oss_helper=oss,
        )

        await service.delete(USER_ID, FILE_INFO_ID)

        self.assertEqual(oss.deleted, [])


if __name__ == "__main__":
    unittest.main()
