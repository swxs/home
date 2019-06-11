# -*- coding: utf-8 -*-

import unittest
from common.Helpers.Helper_validate import Validate, RegType


class ValidateHelperTestCase(unittest.TestCase):
    def test_validate_check_CH(self):
        self.assertTrue(Validate.check("这是中文", reg_type=RegType.CH))
        self.assertFalse(Validate.check("this is english", reg_type=RegType.CH))

    def test_validate_check_mobile(self):
        self.assertTrue(Validate.check("13241651679", reg_type=RegType.MOBILE))
        self.assertFalse(Validate.check("132416516790", reg_type=RegType.MOBILE))

    def test_validate_check_tel(self):
        self.assertTrue(Validate.check("021-51562436", reg_type=RegType.PHONE_COMMON))
        self.assertFalse(Validate.check("021-515624367", reg_type=RegType.PHONE_COMMON))

    def test_validate_check_username(self):
        self.assertTrue(Validate.check("1231-23_", reg_type=RegType.USERNAME))
        self.assertFalse(Validate.check("1231-23_+", reg_type=RegType.USERNAME))

    def test_validate_check_column_id(self):
        self.assertTrue(Validate.check("123123123123123123123123", reg_type=RegType.COLUMN_ID))
        self.assertFalse(Validate.check("12312312312312312312123", reg_type=RegType.COLUMN_ID))

    def test_validate_has(self):
        headers = """Origin: http://localhost:8080
    Content-Length: 13
    Accept-Language: zh-CN,zh;q=0.8
    Accept-Encoding: gzip, deflate, br
    Host: localhost:8080
    Accept: application/json, text/plain, */*
    User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36
    Connection: close
    Cookie: Pycharm-351ef808=6a07f271-f4af-44ff-86c9-3b743c233434; _ga=GA1.1.1168507770.1499048558; _gid=GA1.1.1626334201.1499823835; PYCKET_ID="2|1:0|10:1499849172|9:PYCKET_ID|48:MDdkNzc1YTAtZjY2NC00ZmQ0LTgwNjUtMTJiMTUzYmUwMzAx|6d99e78c025a34ed275430dd1be970b2d9a142a3e516c7149f40441ef4717bc0"; local=zh_CN
    Referer: http://localhost:8080/
    Content-Type: application/x-www-form-urlencoded"""
        self.assertTrue(Validate.has(headers, reg_type=RegType.FORM_GET))

    def test_validate_has_phone(self):
        self.assertTrue(Validate.has("application: multipart/form-data", reg_type=RegType.FORM_FILE))

    def test_validate_start_with_number(self):
        self.assertTrue(Validate.start_with("0123qwe", reg_type=RegType.NUMBER))
        self.assertFalse(Validate.start_with("qwe0123", reg_type=RegType.NUMBER))

    def test_validate_end_with_number(self):
        self.assertTrue(Validate.end_with("qwe0123", reg_type=RegType.NUMBER))
        self.assertFalse(Validate.end_with("0123qwe", reg_type=RegType.NUMBER))

    def test_validate_clear_number(self):
        self.assertEqual(Validate.clear("y1u2r3tyr", reg_type=RegType.NUMBER), "yurtyr")

    def test_validate_getall_number(self):
        self.assertEqual(Validate.get_all("123qwe0123", reg_type=RegType.NUMBER), ["123", "0123"])
