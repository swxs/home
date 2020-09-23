# -*- coding: utf-8 -*-
# @File    : helper_encoder_json_tests.py.py
# @AUTH    : swxs
# @Time    : 2019/1/17 18:07


import unittest
import datetime
from common.Helpers.Helper_Encoder_Json import dumps, loads


class JsonEncoderHelperTestCase(unittest.TestCase):
    def test_dumps_datetime(self):
        json_str = dumps({"datetime": datetime.datetime(2019, 1, 1)})
        self.assertEqual(json_str, '{"datetime": {"val": "2019-01-01 00:00:00", "_spec_type": 43}}')

    def test_loads_datetime(self):
        json_str = loads('{"datetime": {"_spec_type": 43, "val": "2019-01-01 00:00:00"}}')
        self.assertEqual(json_str, {"datetime": datetime.datetime(2019, 1, 1)})

    def test_dumps_npint(self):
        import numpy as np

        json_str = dumps({"npint": np.int(123)})
        self.assertEqual(json_str, '{"npint": 123}')

    def test_loads_npint(self):
        json_str = loads('{"npint": 123}')
        self.assertEqual(json_str, {"npint": 123})
