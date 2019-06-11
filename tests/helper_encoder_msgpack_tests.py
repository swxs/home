# -*- coding: utf-8 -*-
# @File    : helper_encoder_msgpack_tests.py
# @AUTH    : swxs
# @Time    : 2019/1/18 11:18


import unittest
import datetime
from common.Helpers.Helper_Encoder_Msgpack import *


class MsgpackEncoderHelperTestCase(unittest.TestCase):
    def test_dumps_date(self):
        msgpack_str = dumps({"date": datetime.date(2019, 1, 1)})
        self.assertEqual(msgpack_str, b'\x81\xa4date\xc7\n*2019-01-01')

    def test_loads_date(self):
        msgpack_str = loads(b'\x81\xa4date\xc7\n*2019-01-01')
        self.assertEqual(msgpack_str, {b"date": datetime.datetime(2019, 1, 1)})

    def test_dumps_datetime(self):
        msgpack_str = dumps({"datetime": datetime.datetime(2019, 1, 1)})
        self.assertEqual(msgpack_str, b'\x81\xa8datetime\xc7\x13+2019-01-01 00:00:00')

    def test_loads_datetime(self):
        msgpack_str = loads(b'\x81\xa8datetime\xc7\x13+2019-01-01 00:00:00')
        self.assertEqual(msgpack_str, {b"datetime": datetime.datetime(2019, 1, 1, 0, 0)})

    def test_dumps_npint(self):
        import numpy as np
        msgpack_str = dumps({"npint": np.int(123)})
        self.assertEqual(msgpack_str, b'\x81\xa5npint{')

    def test_loads_npint(self):
        msgpack_str = loads(b'\x81\xa5npint{')
        self.assertEqual(msgpack_str, {b"npint": 123})

    def test_dumps_string(self):
        msgpack_str = dumps({"string": "str"})
        self.assertEqual(msgpack_str, b'\x81\xa6string\xa3str')

    def test_loads_string(self):
        msgpack_str = loads(b'\x81\xa6string\xa3str')
        self.assertEqual(msgpack_str, {b"string": b"str"})

    def test_dumps_objectfield(self):
        from bson import ObjectId
        msgpack_str = dumps({"objfield": ObjectId("5c889900c33201480c4228a6")})
        self.assertEqual(msgpack_str, b'\x81\xa8objfield\xc7\x18.5c889900c33201480c4228a6')

    def test_loads_objectfield(self):
        from bson import ObjectId
        msgpack_str = loads(b'\x81\xa8objfield\xc7\x18.5c889900c33201480c4228a6')
        self.assertEqual(msgpack_str, {b"objfield": ObjectId("5c889900c33201480c4228a6")})
