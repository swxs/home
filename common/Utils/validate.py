# -*- coding: utf-8 -*-
import re


class RegType:
    ALL = "all"

    USERNAME = "username"
    PASSWORD = "password"
    CHANGED_PASSWORD = "changed_password"
    MOBILE = "mobile"
    EMAIL = "email"
    PHONE = "phone"
    PHONE_COMMON = "phone_common"

    COLUMN_ID = "column_id"

    FORM_GET = "json_header"
    HTML_TAG = "common_html"
    REQUEST_HEADER = "request_header"

    CH = "CH"
    NUMBER = "number"
    MONTH = "month"
    DAY = "day"
    TIME = "time"
    DATE = "date"
    BIRTHDAY = "birthday"
    CREDIT = "CREDIT"
    URL = "URL"
    IPV4AGENT = "IPV4AGENT"
    IPV4 = "IPV4"
    IPV6 = "IPV6"


class Validate:
    reglist = {
        RegType.COLUMN_ID: r'[a-fA-F0-9]{24}',
        RegType.USERNAME: r'[a-zA-Z0-9_\-]{1,}',
        RegType.PASSWORD: r'[a-zA-Z0-9]{6,}',
        RegType.CHANGED_PASSWORD: r'[0-9a-f]{32}',

        RegType.CH: r'[^\u0000-\u00FF]*',
        RegType.NUMBER: r'([-]?[0-9]+(\.[0-9]+){0,1})',
        RegType.MONTH: r'(0?[1-9]|1[0-2])',
        RegType.DAY: r'((0?[1-9])|((1|2)[0-9])|(3[01]))',
        RegType.TIME: r'(0?[1-9]|1[0-9]|2[0-4])((:|-|\/|\\)(0?[0-9]|[1-5][0-9])){2}',
        RegType.DATE: r'[1-9][0-9]{0,3}(?:年|\||\\|\/|\s|,|、|-)(0?[1-9]|1[0-2])(?:月|\||\\|\/|\s|,|、|-)((0?[1-9])|((1|2)[0-9])|(3[01]))日?',
        RegType.BIRTHDAY: r'(19|20)[0-9]{2}(:|-|\/|\\)(((0?[1-9]|1[0-2])(:|-|\/|\\)(0?[1-9]|1[0-9]|2[0-9]))|((0?[13-9]|1[0-2])(:|-|\/|\\)(30))|((0?[13578]|1[02])(:|-|\/|\\)(31)))',
        RegType.PHONE_COMMON: r'([0-9]{3}[_ -][0-9]{8}|[0-9]{4}-[0-9]{7}|[0-9]{8}|1[0-9]{10})',
        RegType.PHONE: r'(\(((010)|(021)|(0\d{3,4}))\)( ?)([0-9]{7,8}))|((010|021|0\d{3,4}))([- ]?)([0-9]{7,8})|([0-9]{7,8})',
        RegType.MOBILE: r'(1[3-9][0-9])[0-9]{8}',
        RegType.EMAIL: r'([a-zA-Z0-9_\.\-])+\@([a-zA-Z0-9\-])+(\.([a-zA-Z0-9]{2,6}))+',
        RegType.CREDIT: '[1-9][0-9]{5}[1-9][0-9]{3}((0[0-9])|(1[0-2]))(([0|1|2][0-9])|3[0-1])[0-9]{3}([0-9]|x|X)',
        RegType.URL: r'((http|ftp|https)://)?(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}(\.[0-9]{1,3}){3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?',
        RegType.IPV4AGENT: r'(192\.168\.|169\.254\.|10\.|172\.(1[6-9]|2[0-9]|3[01]))',
        RegType.IPV4: r'[0-9]{1,3}(\.[0-9]{1,3}){3}',
        RegType.IPV6: r'[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})',

        RegType.HTML_TAG: r'</?(span|tr|hr|br|p|script)/?>',
        RegType.FORM_GET: r'application/x-www-form-urlencoded',
        RegType.REQUEST_HEADER: r'httputil',

        RegType.ALL: r'.*',
    }

    @classmethod
    def _find_reg(self, reg_type):
        if reg_type in self.reglist:
            return self.reglist[reg_type]
        else:
            # 如果未指定 则……
            return False

    @classmethod
    def has(cls, value, reg_type=RegType.ALL):
        try:
            return re.search(r'{0}'.format(cls._find_reg(reg_type)), value, re.M) is not None
        except TypeError:
            return False

    @classmethod
    def any(cls, value, reg_type_list=None):
        try:
            return any(Validate.has(value, reg_type=reg_type) for reg_type in reg_type_list)
        except TypeError:
            return False

    @classmethod
    def start_with(cls, value, reg_type=RegType.ALL):
        try:
            return re.match(r'^{0}'.format(cls._find_reg(reg_type)), value, re.M) is not None
        except TypeError:
            return False

    @classmethod
    def end_with(cls, value, reg_type=RegType.ALL):
        try:
            return re.match(r'{0}$'.format(cls._find_reg(reg_type)), value, re.M) is not None
        except TypeError:
            return False

    @classmethod
    def check(cls, value, reg_type=RegType.ALL):
        try:
            return re.match(r'^{0}$'.format(cls._find_reg(reg_type)), value, re.M) is not None
        except TypeError:
            return False

    @classmethod
    def clear(cls, value, reg_type=RegType.ALL):
        try:
            return re.sub(r'{0}'.format(cls._find_reg(reg_type)), "", value, re.M)
        except TypeError:
            return False

    @classmethod
    def getall(cls, value, reg_type=RegType.ALL):
        try:
            result = re.findall(r'({0})+'.format(cls._find_reg(reg_type)), value, re.M)
            if len(result) > 0 and isinstance(result[0], tuple):
                return [value[0] for value in result]
            return result
        except TypeError:
            return []


if __name__ == "__main__":
    print(Validate.getall("10ade", RegType.NUMBER))
