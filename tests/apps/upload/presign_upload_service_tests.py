import unittest
from types import SimpleNamespace

from web.exceptions import Http400BadRequestException

from apps.upload.schemas.presign import (
    PresignCompleteRequest,
    PresignUploadRequest,
)
from apps.upload.services.presign_upload_service import PresignUploadService
from apps.upload.storage import build_object_key


USER_ID = "64f000000000000000000001"
FILE_INFO_ID = "65f000000000000000000001"
MD5 = "d41d8cd98f00b204e9800998ecf8427e"
CONTENT_MD5 = "1B2M2Y8AsgTpgAmY7PhCfg=="


class FakeDB:
    async def commit(self):
        return None

    async def rollback(self):
        return None


class FakeRepo:
    def __init__(self):
        self.records = {}
        self.create_calls = 0

    async def find_by_user_content(self, user_id, file_id, file_size):
        return self.records.get((user_id, file_id, file_size))

    async def create_one(self, payload):
        self.create_calls += 1
        values = payload.model_dump()
        values["id"] = FILE_INFO_ID
        record = SimpleNamespace(**values)
        self.records[(record.user_id, record.file_id, record.file_size)] = record
        return record


class FakeOSS:
    def __init__(self):
        self.objects = {}
        self.signed_puts = []

    def exists(self, key):
        return key in self.objects

    def get_file_meta(self, key):
        content_type, size = self.objects[key]
        return 0, content_type, size

    def sign_put_url(self, key, content_type, content_md5, expires):
        self.signed_puts.append((key, content_type, content_md5, expires))
        return f"https://oss.example/{key}"


def upload_request(**overrides):
    values = {
        "file_id": MD5,
        "file_name": "empty.txt",
        "file_size": 0,
        "content_type": "text/plain",
        "content_md5": CONTENT_MD5,
    }
    values.update(overrides)
    return PresignUploadRequest(**values)


class PresignUploadServiceTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.repo = FakeRepo()
        self.oss = FakeOSS()
        self.service = PresignUploadService(
            FakeDB(),
            repo=self.repo,
            oss_helper=self.oss,
            upload_max_bytes=1024,
            upload_expires=600,
        )

    async def test_missing_object_returns_bound_put_url(self):
        request = upload_request(file_size=12)

        result = await self.service.presign_upload(USER_ID, request)

        expected_key = build_object_key(MD5, 12)
        self.assertFalse(result.skip_upload)
        self.assertEqual(result.presigned_url, f"https://oss.example/{expected_key}")
        self.assertEqual(
            self.oss.signed_puts,
            [(expected_key, "text/plain", CONTENT_MD5, 600)],
        )
        self.assertEqual(self.repo.create_calls, 0)

    async def test_existing_object_creates_metadata_and_retries_idempotently(self):
        request = upload_request()
        self.oss.objects[build_object_key(MD5, 0)] = ("text/plain", 0)

        first = await self.service.presign_upload(USER_ID, request)
        second = await self.service.presign_upload(USER_ID, request)

        self.assertTrue(first.skip_upload)
        self.assertEqual(first.data.id, FILE_INFO_ID)
        self.assertEqual(second.data.id, FILE_INFO_ID)
        self.assertEqual(self.repo.create_calls, 1)

    async def test_same_md5_different_sizes_use_different_keys(self):
        first = await self.service.presign_upload(
            USER_ID,
            upload_request(file_size=1),
        )
        second = await self.service.presign_upload(
            USER_ID,
            upload_request(file_size=2),
        )

        self.assertNotEqual(first.presigned_url, second.presigned_url)
        self.assertTrue(first.presigned_url.endswith(f"{MD5[4:]}-1"))
        self.assertTrue(second.presigned_url.endswith(f"{MD5[4:]}-2"))

    async def test_complete_rejects_size_mismatch(self):
        key = build_object_key(MD5, 12)
        self.oss.objects[key] = ("text/plain", 11)
        request = PresignCompleteRequest(
            file_id=MD5,
            file_name="file.txt",
            file_size=12,
            content_type="text/plain",
        )

        with self.assertRaises(Http400BadRequestException):
            await self.service.complete(USER_ID, request)

    async def test_upload_limit_is_enforced_before_signing(self):
        with self.assertRaises(Http400BadRequestException):
            await self.service.presign_upload(
                USER_ID,
                upload_request(file_size=1025),
            )
        self.assertEqual(self.oss.signed_puts, [])

    async def test_content_md5_must_match_file_id(self):
        with self.assertRaises(ValueError):
            upload_request(
                content_md5="XrY7u+Ae7tCTyyK7j1rNww==",
            )


if __name__ == "__main__":
    unittest.main()
