import unittest

from scripts.migrate_file_info_storage import (
    _validate_size,
    build_legacy_object_key,
)

from home.apps.upload.storage import build_object_key


MD5 = "D41D8CD98F00B204E9800998ECF8427E"


class FakeOSS:
    def __init__(self, size):
        self.size = size

    def get_file_meta(self, key):
        return 0, "application/octet-stream", self.size


class FileInfoMigrationTests(unittest.TestCase):
    def test_old_and_new_keys_are_deterministic(self):
        self.assertEqual(
            build_legacy_object_key(MD5),
            "d41d/8cd98f00b204e9800998ecf8427e",
        )
        self.assertEqual(
            build_object_key(MD5, 42),
            "d41d/8cd98f00b204e9800998ecf8427e-42",
        )

    def test_object_size_must_match_before_cleanup(self):
        _validate_size(FakeOSS(42), "new-key", 42)
        with self.assertRaises(ValueError):
            _validate_size(FakeOSS(41), "new-key", 42)


if __name__ == "__main__":
    unittest.main()
