# -*- coding: utf-8 -*-
import re

class Validate:
    reglist = {
        # 'CH': r'[^\u0000-\u00FF]*',
        'number': r'([-]?[0-9]+(\.[0-9]+){0,1})',
        'positive': r'([0-9]+(\.[0-9]+){0,1})',
        'positive_integer': r'([0-9]+)',

        'month': r'(0?[1-9]|1[0-2])',
        'day': r'((0?[1-9])|((1|2)[0-9])|(3[01]))',
        'time': r'(0?[1-9]|1[0-9]|2[0-4])((:|-|\/|\\)(0?[0-9]|[1-5][0-9])){2}',

        'username': r'[a-zA-Z0-9_\-]{1,}',
        'password': r'[a-zA-Z0-9]{6,}',
        'password_easy': r'.{6,16}',
        'password_hard': r'(?=.*[0-9])(?=.*[a-zA-Z])(.{6,12})',

        'date': r'[1-9][0-9]{0,3}(?:年|\||\\|\/|\s|,|、|-)(0?[1-9]|1[0-2])(?:月|\||\\|\/|\s|,|、|-)((0?[1-9])|((1|2)[0-9])|(3[01]))日?',
        'birthday': r'(19|20)[0-9]{2}(:|-|\/|\\)(((0?[1-9]|1[0-2])(:|-|\/|\\)(0?[1-9]|1[0-9]|2[0-9]))|((0?[13-9]|1[0-2])(:|-|\/|\\)(30))|((0?[13578]|1[02])(:|-|\/|\\)(31)))',
        'birthday_hard': r'(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)',

        'credit': '[1-9][0-9]{5}[1-9][0-9]{3}((0[0-9])|(1[0-2]))(([0|1|2][0-9])|3[0-1])[0-9]{3}([0-9]|x|X)',
        # 'carcode': '[\u4E00-\u9FA5]{1}[A-Z]{1}[A-Z0-9]{5}',

        'qq': r'[1-9][0-9]{4,}',
        'fax': r'^[+]{0,1}([0-9]){1,3}[ ]?([-]?(([0-9])|[ ]){1,12})+',
        'phone_common': r'([0-9]{3}-[0-9]{8}|[0-9]{4}-[0-9]{7}|[0-9]{8}|1[0-9]{10})',
        'phone': r'(\(((010)|(021)|(0\d{3,4}))\)( ?)([0-9]{7,8}))|((010|021|0\d{3,4}))([- ]{1,2})([0-9]{7,8})',
        'mobile': r'((13[0-9])|147|(15[0-35-9])|180|182|(18[5-9]))[0-9]{8}',

        'email': r'([a-zA-Z0-9_\.\-])+\@([a-zA-Z0-9\-])+(\.([a-zA-Z0-9]{2,6}))+',
        'url': r'(([a-zA-Z]+)(:\/\/))?([a-zA-Z]+)\.(\w+)\.([\w.]+)(\/([\w]+)\/?)*(\/[a-zA-Z0-9]+\.(\w+))*(\/([\w]+)\/?)*(\?(\w+=?[\w]*))*((&?\w+=?[\w]*))*',
        'URL': r'((http|ftp|https)://)?(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}(\.[0-9]{1,3}){3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?',
        'ipv4Agent': r'(192\.168\.|169\.254\.|10\.|172\.(1[6-9]|2[0-9]|3[01]))',
        'ipv4': r'[0-9]{1,3}(\.[0-9]{1,3}){3}',
        'ipv6': r'[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})',
        'column_id': r'[a-fA-F0-9]{24}',

        'json_header': r'application/x-www-form-urlencoded',
        'request_header': r'httputil',
        'AGGFUNC_COUNT': r'count',
        'AGGFUNC_NUNIQ': r'nuniq',
        'AGGFUNC_SUM': r'sum',
        'AGGFUNC_MEAN': r'mean',
        'AGGFUN_MEDIAN': r'median',
        'AGGFUNC_MAX': r'max',
        'AGGFUNC_MIN': r'min',
        'AGGFUNC_ABS': r'abs',
        'AGGFUNC_PROD': r'prod',
        'AGGFUNC_STD': r'std',
        'AGGFUNC_VAR': r'var',
        'AGGFUNC_SEM': r'sem',
        'AGGFUNC_SKEW': r'skew',
        'AGGFUNC_KURT': r'kurt',
        'AGGFUNC_QUANTILE': r'quantile',
        'AGGFUNC_CUMSUM': r'cumsum',
        'AGGFUNC_CUMPROD': r'cumprod',
        'AGGFUNC_LEN': r'len',
        'AGGFUNC_FAV_RATE': r'fav_rate',
        'all': r'.*',
    }

    @classmethod
    def _find_reg(self, reg_type):
        if reg_type in self.reglist:
            return self.reglist[reg_type]
        else:
            # 如果未指定 则……
            return False

    @classmethod
    def check(cls, value, reg_type="all"):
        try:
            return re.match(r'^{0}$'.format(cls._find_reg(reg_type)), value, re.M) is not None
        except TypeError:
            return False

    @classmethod
    def has(cls, value, reg_type="all"):
        try:
            return re.search(r'{0}'.format(cls._find_reg(reg_type)), value, re.M) is not None
        except TypeError:
            return False

    @classmethod
    def any(cls, value, reg_type_list=None):
        try:
            for reg_type in reg_type_list:
                if Validate.has(value, reg_type=reg_type):
                    return True
            return False
        except TypeError:
            return False