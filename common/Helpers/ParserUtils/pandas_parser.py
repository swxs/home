# -*- coding: utf-8 -*-
# @File    : pandas_parser.py.py
# @AUTH    : swxs
# @Time    : 2018/11/5 9:37

import uuid
import datetime
import weakref
from collections import deque, namedtuple
from .calc_lexer import (yacc, calcLexer)
from .parser_exception import SyntaxException
from tornado.util import ObjectDict
from apps.bi import model_enums

RTYPE_COLUMN = "COLUMN"
RTYPE_SERIES = "SERIES"
RTYPE_RAW = "RAW"
RTYPE_AGG = "AGG"
DTYPE_BOOL = "BOOL"
DTYPE_STRING = "STRING"
DTYPE_NUMBER = "NUMBER"
DTYPE_DATETIME = "DATETIME"


def _format_value(temp):
    '''
    用于把数值类型的字符串转为float类型
    :param temp: 要转换的字符串
    :param field_dict:
    :return:
    '''
    if not isinstance(temp, str):
        return temp
    elif temp.isdigit():
        return float(temp)
    else:
        return temp


class Result(object):
    def __init__(self, result, steps):
        self.result = result
        self.steps = steps

    def __str__(self):
        return str(self.result)


class ValueGroup(object):
    def __init__(self):
        self._value_groups = list()
    
    def append(self, groups):
        self._value_groups.append(groups)
    
    def __iter__(self):
        for value in self._value_groups:
            yield value

    def __str__(self):
        return "\n".join(str(group) for group in self._value_groups[::-1])


class Group(object):
    def __init__(self, expression, value):
        if value.rtype not in (RTYPE_RAW, ):
            raise SyntaxException(msg="分组类型需要时基本类型")
        self.expression = expression
        self.value = value

    def __str__(self):
        return f"{self.expression} => {self.value}"


class NodeList(object):
    def __init__(self, node):
        self.nodes = []
        self.append(node)

    def append(self, node):
        _node = self.check_node(node)
        self.nodes.append(_node)
    
    def check_node(self, node):
        pass
        return node

    def __str__(self):
        return ", ".join(str(node) for node in self.nodes)


class Command(object):
    def __init__(self, parser, command):
        self.parser = parser
        if isinstance(command, CalcFirst):
            self.command = command.value
        else:
            self.command = command
        self.rtype = command.rtype
        self.dtype = command.dtype

        if isinstance(self.command, Aggregate):
            self.raw = self.command
        elif isinstance(self.command, Calc):
            self.raw = self.command
            if self.command.rtype != RTYPE_AGG:
                self.col = str(uuid.uuid4())
                self.parser.codes.append((self.col, str(self.command)))
        elif isinstance(self.command, Number):
            self.raw = self.command.raw
            self.col = str(uuid.uuid4())
            self.parser.codes.append((self.col, self.command.raw))
        elif isinstance(self.command, String):
            self.raw = self.command.raw
            self.col = str(uuid.uuid4())
            self.parser.codes.append((self.col, self.command.raw))
        elif isinstance(self.command, Column):
            self.raw = self.command.raw
            self.col = str(uuid.uuid4())
            self.parser.codes.append((self.col, f"df[{self.command}]"))

    def __str__(self):
        if isinstance(self.command, Aggregate):
            return str(self.raw)
        elif isinstance(self.command, Calc):
            if self.command.rtype == RTYPE_AGG:
                return str(self.raw)
            else:
                return f"'{self.col}'"
        else:
            return f"'{self.col}'"


class Column(object):
    def __init__(self, column):
        self.raw = column
        self.rtype = RTYPE_COLUMN
        if self.raw.dtype in (
            model_enums.COLUMN_DTYPE_STRING,
            model_enums.COLUMN_DTYPE_LONGTEXT,
            model_enums.COLUMN_DTYPE_OBJECT,
            model_enums.COLUMN_DTYPE_GROUP,
        ):
            self.dtype = DTYPE_STRING
        elif self.raw.dtype in (
            model_enums.COLUMN_DTYPE_INT, 
            model_enums.COLUMN_DTYPE_FLOAT,
        ):
            self.dtype = DTYPE_NUMBER
        elif self.raw.dtype in (
            model_enums.COLUMN_DTYPE_DATETIME,
        ):
            self.dtype = DTYPE_DATETIME
        else:
            raise SyntaxException(msg="字段类型非法")
        self.col = self.raw.col

    def __str__(self):
        return f"'{self.col}'"


class Number(object):
    def __init__(self, number):
        self.raw = number
        self.rtype = RTYPE_RAW
        self.dtype = DTYPE_NUMBER
    
    def __str__(self):
        return str(float(self.raw))


class String(object):
    def __init__(self, string):
        self.raw = string
        self.rtype = RTYPE_RAW
        self.dtype = DTYPE_STRING
    
    def __str__(self):
        return f"{self.raw}"


class Part(object):
    def __init__(self, ttype, children):
        self.ttype = ttype
        self.rtype = RTYPE_SERIES
        self.dtype = DTYPE_BOOL
        self.children = children

    def __str__(self):
        return f"(({self.children[0]}){self.ttype}({self.children[1]}))"


class Calc(object):
    def __init__(self, ttype, left, right):
        self.ttype = ttype
        self.left = left
        self.right = right
        if self.left.rtype in (RTYPE_COLUMN, RTYPE_SERIES) and self.right.rtype in (RTYPE_COLUMN, RTYPE_SERIES, RTYPE_RAW):
            self.rtype = RTYPE_SERIES
        elif self.left.rtype in (RTYPE_COLUMN, RTYPE_SERIES, RTYPE_RAW) and self.right.rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            self.rtype = RTYPE_SERIES
        elif self.left.rtype in (RTYPE_AGG, ) and self.right.rtype in (RTYPE_AGG, RTYPE_RAW):
            self.rtype = RTYPE_AGG
        elif self.left.rtype in (RTYPE_AGG, RTYPE_RAW) and self.right.rtype in (RTYPE_AGG, ):
            self.rtype = RTYPE_AGG
        elif self.left.rtype in (RTYPE_RAW, ) and self.right.rtype in (RTYPE_RAW, ):
            self.rtype = RTYPE_RAW
        else:
            raise SyntaxException(msg="计算类型非法")
        self.dtype = DTYPE_NUMBER

    def __str__(self):
        left_part = f'df[{self.left}]' if self.left.rtype in (RTYPE_COLUMN, RTYPE_SERIES) else self.left
        right_part = f'df[{self.right}]' if self.right.rtype in (RTYPE_COLUMN, RTYPE_SERIES) else self.right
        return f"{left_part} {self.ttype} {right_part}"


class CalcFirst(object):
    def __init__(self, value):
        self.value = value
        self.rtype = value.rtype
        self.dtype = value.dtype

    def __str__(self):
        return f"({self.value})"


class Filter(object):
    def __init__(self, ttype, left, right):
        self.ttype = ttype
        self.left = left
        self.right = right
        self.rtype = RTYPE_SERIES
        self.dtype = DTYPE_BOOL

    def __str__(self):
        left_part = f'df[{self.left}]' if self.left.rtype in (RTYPE_COLUMN, ) else self.left
        right_part = f'df[{self.right}]' if self.right.rtype in (RTYPE_COLUMN, ) else self.right
        return f"{left_part} {self.ttype} {right_part}"


class Function(object):
    def __init__(self, parser, node_list):
        self.parser = parser
        self.node_list = node_list
        self.col = str(uuid.uuid4())
    
    def __str__(self):
        return f"'{self.col}'"

class MEANIF(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[1].rtype == RTYPE_SERIES and \
            self.node_list[1].dtype == DTYPE_BOOL:
            self.select = self.node_list[0]
            self.part = self.node_list[1]
            # self.parser.codes.append((self.col, f"(df.loc[({self.part}), {self.select}]).mean()"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("MEAFIF参数类型非法")
    
    def __str__(self):
        return f"(df.loc[({self.part}), {self.select}]).mean()"

class SUMIF(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[1].rtype == RTYPE_SERIES and \
            self.node_list[1].dtype == DTYPE_BOOL:
            self.select = self.node_list[0]
            self.part = self.node_list[1]
            # self.parser.codes.append((self.col, f"(df.loc[({self.part}), {self.select}]).sum()"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("SUMIF参数类型非法")
    
    def __str__(self):
        return f"(df.loc[({self.part}), {self.select}]).sum()"
    
class COUNTIF(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[1].rtype == RTYPE_SERIES and \
            self.node_list[1].dtype == DTYPE_BOOL:
            self.select = self.node_list[0]
            self.part = self.node_list[1]
            # self.parser.codes.append((self.col, f"(df.loc[({self.part}), {self.select}]).count()"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("COUNTIF参数类型非法")
    
    def __str__(self):
        return f"(df.loc[({self.part}), {self.select}]).count()"

class DISTINCTIF(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[1].rtype == RTYPE_SERIES and \
            self.node_list[1].dtype == DTYPE_BOOL:
            self.select = self.node_list[0]
            self.part = self.node_list[1]
            # self.parser.codes.append((self.col, f"(df.loc[({self.part}), {self.select}]).nunique()"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("DISTINCTIF参数类型非法")
    
    def __str__(self):
        return f"(df.loc[({self.part}), {self.select}]).nunique()"

class PERCENTILEIF(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[1].rtype == RTYPE_RAW and \
            self.node_list[1].dtype == DTYPE_NUMBER and \
            self.node_list[2].rtype == RTYPE_SERIES and \
            self.node_list[2].dtype == DTYPE_BOOL:
            self.select = self.node_list[0]
            self.number = self.node_list[1]
            self.part = self.node_list[2]
            # self.parser.codes.append((self.col, f"(df.loc[({self.part}), {self.select}]).quantile(q={self.number})"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("PERCENTILEIF参数类型非法")
    
    def __str__(self):
        return f"(df.loc[({self.part}), {self.select}]).quantile(q={self.number})"
    
class MAXIF(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[1].rtype == RTYPE_SERIES and \
            self.node_list[1].dtype == DTYPE_BOOL:
            self.select = self.node_list[0]
            self.part = self.node_list[1]
            # self.parser.codes.append((self.col, f"(df.loc[({self.part}), {self.select}]).nlargest(1)"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("MAXIF参数类型非法")
    
    def __str__(self):
        return f"(df.loc[({self.part}), {self.select}]).nlargest(1).iloc[0]"

class MINIF(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[1].rtype == RTYPE_SERIES and \
            self.node_list[1].dtype == DTYPE_BOOL:
            self.select = self.node_list[0]
            self.part = self.node_list[1]
            # self.parser.codes.append((self.col, f"(df.loc[({self.part}), {self.select}]).nsmallest(1)"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("MINIF参数类型非法")
    
    def __str__(self):
        return f"(df.loc[({self.part}), {self.select}]).nsmallest(1).iloc[0]"

class AVG(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_NUMBER:
            self.select = self.node_list[0]
            # self.parser.codes.append((self.col, f"(df.loc[:, {self.select}]).mean()"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("AVG参数类型非法")
    
    def __str__(self):
        return f"(df.loc[:, {self.select}]).mean()"
    
class SUM(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_NUMBER:
            self.select = self.node_list[0]
            # self.parser.codes.append((self.col, f"(df.loc[:, {self.select}]).sum()"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("SUM参数类型非法")
    
    def __str__(self):
        return f"(df.loc[:, {self.select}]).sum()"
    
class COUNT(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype != DTYPE_BOOL:
            self.select = self.node_list[0]
            # self.parser.codes.append((self.col, f"(df.loc[:, {self.select}]).count()"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("COUNT参数类型非法")
    
    def __str__(self):
        return f"(df.loc[:, {self.select}]).count()"

class DISTINCT(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype != DTYPE_BOOL:
            self.select = self.node_list[0]
            # self.parser.codes.append((self.col, f"(df.loc[:, {self.select}]).nunique()"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("DISTINCT参数类型非法")
    
    def __str__(self):
        return f"(df.loc[:, {self.select}]).nunique()"

class PERCENTILE(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[1].rtype == RTYPE_RAW and \
            self.node_list[1].dtype == DTYPE_NUMBER:
            self.select = node_list[0]
            self.number = node_list[1]
            # self.parser.codes.append((self.col, f"(df.loc[:, {self.select}]).quantile(q={self.number})"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("PERCENTILE参数类型非法")
    
    def __str__(self):
        return f"(df.loc[:, {self.select}]).quantile(q={self.number})"

class MAX(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_NUMBER:
            self.select = self.node_list[0]
            # self.parser.codes.append((self.col, f"(df.loc[:, {self.select}]).nlargest(1)"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("MAX参数类型非法")
    
    def __str__(self):
        return f"(df.loc[:, {self.select}]).nlargest(1).iloc[0]"
    
class MIN(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_NUMBER:
            self.select = self.node_list[0]
            # self.parser.codes.append((self.col, f"(df.loc[:, {self.select}]).nsmallest(1)"))
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("MIN参数类型非法")
    
    def __str__(self):
        return f"(df.loc[:, {self.select}]).nsmallest(1).iloc[0]"
    
class GREATEST(Function):
    def _get_params(self, value):
        if value.rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            return f"x[{value}]"
        elif value.rtype in (RTYPE_RAW, ):
            return f"{value}"
        else:
            raise SyntaxException("GREATEST参数类型非法")

    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        for arg in self.node_list:
            if (arg.dtype != DTYPE_NUMBER) or (arg.rtype == RTYPE_AGG):
                raise SyntaxException()
        params = ", ".join(self._get_params(args) for args in self.node_list)
        self.parser.codes.append((self.col, f"df.apply(lambda x: max({params}), axis=1)"))
        self.rtype = RTYPE_SERIES
        self.dtype = DTYPE_NUMBER

class LEAST(Function):
    def _get_params(self, value):
        if value.rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            return f"x[{value}]"
        elif value.rtype in (RTYPE_RAW, ):
            return f"{value}"
        else:
            raise SyntaxException("LEAST参数类型非法")

    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        for arg in self.node_list:
            if (arg.dtype != DTYPE_NUMBER) or (arg.rtype == RTYPE_AGG):
                raise SyntaxException()
        params = ", ".join(self._get_params(args) for args in self.node_list)
        self.parser.codes.append((self.col, f"df.apply(lambda x: min({params}), axis=1)"))
        self.rtype = RTYPE_SERIES
        self.dtype = DTYPE_NUMBER

class ABS(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"(df.loc[:, {self.select}]).abs()"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        elif self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_RAW, RTYPE_AGG):
            self.select = self.node_list[0]
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
            self.string = f"np.abs({self.select})"
        else:
            raise SyntaxException("ABS参数类型非法")
    
    def __str__(self):
        if self.rtype == RTYPE_AGG:
            return self.string
        else:
            return f"'{self.col}'"

class CEIL(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df.apply(lambda x: np.ceil(x[{self.select}]), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        elif self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_RAW, RTYPE_AGG):
            self.select = self.node_list[0]
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
            self.string = f"np.ceil({self.select})"
        else:
            raise SyntaxException("CEIL参数类型非法")
    
    def __str__(self):
        if self.rtype == RTYPE_AGG:
            return self.string
        else:
            return f"'{self.col}'"

class FLOOR(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df.apply(lambda x: np.floor(x[{self.select}]), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        elif self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_RAW, RTYPE_AGG):
            self.select = self.node_list[0]
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
            self.string = f"np.floor({self.select})"
        else:
            raise SyntaxException("FLOOR参数类型非法")
    
    def __str__(self):
        if self.rtype == RTYPE_AGG:
            return self.string
        else:
            return f"'{self.col}'"

class LN(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df.apply(lambda x: math.log(x[{self.select}], np.e), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        elif self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_RAW, RTYPE_AGG):
            self.select = self.node_list[0]
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
            self.string = f"math.log({self.select}, np.e)"
        else:
            raise SyntaxException("LN参数类型非法")

    def __str__(self):
        if self.rtype == RTYPE_AGG:
            return self.string
        else:
            return f"'{self.col}'"

class LOG(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if len(self.node_list) == 2 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[1].dtype == DTYPE_NUMBER and \
            self.node_list[1].rtype in (RTYPE_RAW, ):
            self.select = self.node_list[0]
            self.number = self.node_list[1]
            self.parser.codes.append((self.col, f"df.apply(lambda x: math.log(x[{self.select}], {self.number}), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        elif len(self.node_list) == 1 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df.apply(lambda x: math.log(x[{self.select}], 10), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        elif len(self.node_list) == 2 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_RAW, RTYPE_AGG) and \
            self.node_list[1].dtype == DTYPE_NUMBER and \
            self.node_list[1].rtype in (RTYPE_RAW, ):
            self.select = self.node_list[0]
            self.number = self.node_list[1]
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
            self.string = f"math.log({self.select}, {self.number})"
        elif len(self.node_list) == 1 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_RAW, RTYPE_AGG):
            self.select = self.node_list[0]
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
            self.string = f"math.log({self.select}, 10)"
        else:
            raise SyntaxException("LOG参数类型非法")
    
    def __str__(self):
        if self.rtype == RTYPE_AGG:
            return self.string
        else:
            return f"'{self.col}'"

class POW(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if len(self.node_list) == 2 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[1].dtype == DTYPE_NUMBER and \
            self.node_list[1].rtype in (RTYPE_RAW, ):
            self.select = self.node_list[0]
            self.number = self.node_list[1]
            self.parser.codes.append((self.col, f"df.apply(lambda x: math.pow(x[{self.select}], {self.number}), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        elif len(self.node_list) == 1 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df.apply(lambda x: math.pow(x[{self.select}], 2), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        elif len(self.node_list) == 2 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_RAW, RTYPE_AGG) and \
            self.node_list[1].dtype == DTYPE_NUMBER and \
            self.node_list[1].rtype in (RTYPE_RAW, ):
            self.select = self.node_list[0]
            self.number = self.node_list[1]
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
            self.string = f"math.pow({self.select}, {self.number})"
        elif len(self.node_list) == 1 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_RAW, RTYPE_AGG):
            self.select = self.node_list[0]
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
            self.string = f"math.pow({self.select}, 2)"
        else:
            raise SyntaxException("POW参数类型非法")
    
    def __str__(self):
        if self.rtype == RTYPE_AGG:
            return self.string
        else:
            return f"'{self.col}'"

class ROUND(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if len(self.node_list) == 2 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[1].dtype == DTYPE_NUMBER and \
            self.node_list[1].rtype in (RTYPE_RAW, ):
            self.select = self.node_list[0]
            self.number = self.node_list[1]
            self.parser.codes.append((self.col, f"df.apply(lambda x: np.round(x[{self.select}], int({self.number})), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        elif len(self.node_list) == 1 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df.apply(lambda x: np.round(x[{self.select}], 2), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        elif len(self.node_list) == 2 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_RAW, RTYPE_AGG) and \
            self.node_list[1].dtype == DTYPE_NUMBER and \
            self.node_list[1].rtype in (RTYPE_RAW, ):
            self.select = self.node_list[0]
            self.number = self.node_list[1]
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
            self.string = f"np.round({self.select}, int({self.number}))"
        elif len(self.node_list) == 1 and \
            self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_RAW, RTYPE_AGG):
            self.select = self.node_list[0]
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
            self.string = f"np.round({self.select}, 2)"
        else:
            raise SyntaxException("ROUND参数类型非法")
    
    def __str__(self):
        if self.rtype == RTYPE_AGG:
            return self.string
        else:
            return f"'{self.col}'"

class SQRT(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df.apply(lambda x: math.sqrt(x[{self.select}]), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        elif self.node_list[0].dtype == DTYPE_NUMBER and \
            self.node_list[0].rtype in (RTYPE_RAW, RTYPE_AGG):
            self.select = self.node_list[0]
            self.rtype = RTYPE_AGG
            self.dtype = DTYPE_NUMBER
            self.string = f"math.sqrt({self.select})"
        else:
            raise SyntaxException("SQRT参数类型非法")
    
    def __str__(self):
        if self.rtype == RTYPE_AGG:
            return self.string
        else:
            return f"'{self.col}'"

class DATEDIFF(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_RAW, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME and \
            self.node_list[1].rtype in (RTYPE_COLUMN, RTYPE_RAW, RTYPE_SERIES) and \
            self.node_list[1].dtype == DTYPE_DATETIME:
            self.select = self.node_list[0]
            self.tmp = self.node_list[1]
            self.parser.codes.append((self.col, f"df.apply(lambda x: (x[{self.select}] - x[{self.tmp}]).days, axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("DATEDIFF参数类型非法")

class DATEADD(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME and \
            self.node_list[1].rtype in (RTYPE_RAW, ) and \
            self.node_list[1].dtype == DTYPE_NUMBER:
            self.select = self.node_list[0]
            self.tmp = self.node_list[1]
            self.parser.codes.append((self.col, f"df.apply(lambda x: x[{self.select}] + datetime.timedelta(days={self.tmp}), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_DATETIME
        else:
            raise SyntaxException("DATEADD参数类型非法")
    
class DATESUB(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME and \
            self.node_list[1].rtype in (RTYPE_RAW, ) and \
            self.node_list[1].dtype == DTYPE_NUMBER:
            self.select = self.node_list[0]
            self.tmp = self.node_list[1]
            self.parser.codes.append((self.col, f"df.apply(lambda x: x[{self.select}] - datetime.timedelta(days={self.tmp}), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_DATETIME
        else:
            raise SyntaxException("DATESUB参数类型非法")

class DATETRUNC(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_RAW, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME and \
            self.node_list[1].rtype == RTYPE_RAW and \
            self.node_list[1].dtype == DTYPE_STRING:
            self.select = self.node_list[0]
            self.tmp = self.node_list[1]
            if self.node_list[1].raw == '"year"':
                self.parser.codes.append((self.col, f"df.apply(lambda x: x[{self.select}] - datetime.timedelta(days=(x[{self.select}].dayofyear - 1)), axis=1)"))
            elif self.node_list[1].raw == '"month"':
                self.parser.codes.append((self.col, f"df.apply(lambda x: x[{self.select}] - datetime.timedelta(days=(x[{self.select}].day - 1)), axis=1)"))
            elif self.node_list[1].raw == '"week"':
                self.parser.codes.append((self.col, f"df.apply(lambda x: x[{self.select}] - datetime.timedelta(days=(x[{self.select}].dayofweek - 1)), axis=1)"))
            else:
                raise SyntaxException("DATETRUNC参数类型非法， 请输入\"year\", \"month\", \"week\"其中之一")
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_DATETIME
        else:
            raise SyntaxException("DATETRUNC参数类型非法")

class DAY(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df[{self.select}].dt.day"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("DAY参数类型非法")

class LASTDAY(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df.apply(lambda x: x[{self.select}] + datetime.timedelta(days=(x[{self.select}].daysinmonth - x[{self.select}].day)), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_DATETIME
        else:
            raise SyntaxException("LASTDAY参数类型非法")

class MONTH(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df[{self.select}].dt.month"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("MONTH参数类型非法")
    
class MONTHSBETWEEN(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_RAW, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME and \
            self.node_list[1].rtype in (RTYPE_COLUMN, RTYPE_RAW, RTYPE_SERIES) and \
            self.node_list[1].dtype == DTYPE_DATETIME:
            self.select = self.node_list[0]
            self.tmp = self.node_list[1]
            self.parser.codes.append((self.col, f"df.apply(lambda x: (x[{self.select}] - x[{self.tmp}]).days // 7, axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("MONTHSBETWEEN参数类型非法")

class QUARTER(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df[{self.select}].dt.quarter"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("QUARTER参数类型非法")
    
class TODATE(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"pd.to_datetime(df[{self.select}])"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_DATETIME
        elif self.node_list[0].rtype in (RTYPE_RAW, ) and \
            self.node_list[0].dtype == DTYPE_STRING:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"pd.to_datetime({self.select})"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_DATETIME
        else:
            raise SyntaxException("TODATE参数类型非法")
    
class WEEKOFYEAR(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df[{self.select}].dt.weekofyear"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("WEEKOFYEAR参数类型非法")
    
class YEAR(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].rtype in (RTYPE_COLUMN, RTYPE_SERIES) and \
            self.node_list[0].dtype == DTYPE_DATETIME:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df[{self.select}].dt.year"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("YEAR参数类型非法")

class CONCAT(Function):
    def _get_params(self, value):
        if value.rtype in (RTYPE_COLUMN, RTYPE_SERIES):
            return f"df[{value}]"
        elif value.rtype in (RTYPE_RAW, ):
            return f"{value}"
        else:
            raise SyntaxException("CONCAT参数类型非法")

    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        for arg in self.node_list:
            if (arg.dtype != DTYPE_STRING) or (arg.rtype == RTYPE_AGG):
                raise SyntaxException("CONCAT参数类型非法")
        self.select = self.node_list[0]
        params = ", ".join(self._get_params(args) for args in self.node_list[1:])
        self.parser.codes.append((self.col, f"df[{self.select}].str.cat({params})"))
        self.rtype = RTYPE_SERIES
        self.dtype = DTYPE_STRING

class INSTR(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if len(self.node_list) == 2 and \
            self.node_list[0].dtype == DTYPE_STRING and \
            self.node_list[1].rtype == RTYPE_RAW and \
            self.node_list[1].dtype == DTYPE_STRING:
            self.select = self.node_list[0]
            self.check = self.node_list[1]
            self.parser.codes.append((self.col, f"df[{self.select}].str.find({self.check}) + 1"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("INSTR参数类型非法")

class LENGTH(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].dtype == DTYPE_STRING:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df[{self.select}].str.len()"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_NUMBER
        else:
            raise SyntaxException("LENGTH参数类型非法")

class LOWER(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].dtype == DTYPE_STRING:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df[{self.select}].str.lower()"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_STRING
        else:
            raise SyntaxException("LOWER参数类型非法")

class UPPER(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if self.node_list[0].dtype == DTYPE_STRING:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df[{self.select}].str.upper()"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_STRING
        else:
            raise SyntaxException("UPPER参数类型非法")
    
class REGEXPEXTRACT(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        raise SyntaxException("REGEXPREPLACE， 本函数当前未支持")
    
    def __str__(self):
        return ""

class REGEXPREPLACE(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if len(self.node_list) == 3 and \
            self.node_list[0].dtype == DTYPE_STRING and \
            self.node_list[1].rtype == RTYPE_RAW and \
            self.node_list[1].dtype == DTYPE_STRING and \
            self.node_list[2].rtype == RTYPE_RAW and \
            self.node_list[2].dtype == DTYPE_STRING:
            self.select = self.node_list[0]
            self.regexp = self.node_list[1]
            self.replace = self.node_list[2]
            self.parser.codes.append((self.col, f"df[{self.select}].str.replace({self.regexp}, {self.replace}, regex=True)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_STRING
        else:
            raise SyntaxException("REGEXPREPLACE参数类型非法")
    
class REPEAT(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if len(self.node_list) < 2:
            raise SyntaxException("REPEAT参数类型过少， 最少需要两个")
        if self.node_list[0].dtype == DTYPE_STRING and \
            self.node_list[1].rtype == RTYPE_RAW and \
            self.node_list[1].dtype == DTYPE_NUMBER:
            self.select = self.node_list[0]
            self.number = self.node_list[1]
            self.parser.codes.append((self.col, f"df[{self.select}].str.repeat(int({self.number}))"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_STRING
        else:
            raise SyntaxException("REPEAT参数类型非法")
    
class REVERSE(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if len(self.node_list) == 1 and \
            self.node_list[0].dtype == DTYPE_STRING:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df[{self.select}].str.slice(step=-1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_STRING
        else:
            raise SyntaxException("REVERSE参数类型非法")

class SUBSTR(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if len(self.node_list) == 3 and \
            self.node_list[0].dtype == DTYPE_STRING and \
            self.node_list[1].rtype == RTYPE_RAW and \
            self.node_list[1].dtype == DTYPE_NUMBER and \
            self.node_list[2].dtype == RTYPE_RAW and \
            self.node_list[2].dtype == DTYPE_NUMBER:
            self.select = self.node_list[0]
            self.start = self.node_list[1]
            self.length = self.node_list[2]
            self.parser.codes.append((self.col, f"df[{self.select}].str.slice(int({self.start}), ({self.length}))"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_STRING
        elif len(self.node_list) == 2 and \
            self.node_list[0].dtype == DTYPE_STRING and \
            self.node_list[1].rtype == RTYPE_RAW and \
            self.node_list[1].dtype == DTYPE_NUMBER:
            self.select = self.node_list[0]
            self.start = self.node_list[1]
            self.parser.codes.append((self.col, f"df[{self.select}].str.slice(int({self.start}))"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_STRING
        else:
            raise SyntaxException("SUBSTR参数类型非法")
    
class TRIM(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if len(self.node_list) == 1 and \
            self.node_list[0].dtype == DTYPE_STRING:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df[{self.select}].str.strip()"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_STRING
        else:
            raise SyntaxException("TRIM参数类型非法")

class UNBASE64(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if len(self.node_list) == 1 and \
            self.node_list[0].dtype == DTYPE_STRING:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df.apply(lambda x: base64.b64decode(x[{self.select}].encode()).decode('utf8'), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_STRING
        else:
            raise SyntaxException("UNBASE64参数类型非法")

class BASE64(Function):
    def __init__(self, parser, node_list):
        super().__init__(parser, node_list)
        if len(self.node_list) == 1 and \
            self.node_list[0].dtype == DTYPE_STRING:
            self.select = self.node_list[0]
            self.parser.codes.append((self.col, f"df.apply(lambda x: base64.b64encode(x[{self.select}].encode()).decode('utf8'), axis=1)"))
            self.rtype = RTYPE_SERIES
            self.dtype = DTYPE_STRING
        else:
            raise SyntaxException("BASE64参数类型非法")
    
FunctionDict = {
    "AVG": AVG,
    "MEAN": AVG,
    "COUNT": COUNT,
    "DISTINCT": DISTINCT,
    "MAX": MAX,
    "MIN": MIN,
    "PERCENTILE": PERCENTILE,
    "SUM": SUM,
    "AVGIF": MEANIF,
    "MEANIF": MEANIF,
    "COUNTIF": COUNTIF,
    "DISTINCTIF": DISTINCTIF,
    "MAXIF": MAXIF,
    "MINIF": MINIF,
    "PERCENTILEIF": PERCENTILEIF,
    "SUMIF": SUMIF,
    "GREATEST": GREATEST,
    "LEAST": LEAST,
    "DATEDIFF": DATEDIFF,
    "DATEADD": DATEADD,
    "DATESUB": DATESUB,
    "DATETRUNC": DATETRUNC,
    "DAY": DAY,
    "LASTDAY": LASTDAY,
    "MONTH": MONTH,
    "MONTHSBETWEEN": MONTHSBETWEEN,
    "QUARTER": QUARTER,
    "TODATE": TODATE,
    "WEEKOFYEAR": WEEKOFYEAR,
    "YEAR": YEAR,
    "BASE64": BASE64,
    "CONCAT": CONCAT,
    "INSTR": INSTR,
    "LENGTH": LENGTH,
    "LOWER": LOWER,
    "REGEXPEXTRACT": REGEXPEXTRACT,
    "REGEXPREPLACE": REGEXPREPLACE,
    "REPEAT": REPEAT,
    "REVERSE": REVERSE,
    "SUBSTR": SUBSTR,
    "TRIM": TRIM,
    "UNBASE64": UNBASE64,
    "UPPER": UPPER,
    "ABS": ABS,
    "CEIL": CEIL,
    "FLOOR": FLOOR,
    "LN": LN,
    "LOG": LOG,
    "POW": POW,
    "ROUND": ROUND,
    "SQRT": SQRT,
}

class Aggregate(object):
    def __init__(self, parser, ttype, node_list):
        self.parser = parser
        self.ttype = ttype
        self.raw = None
        self.node_list = node_list.nodes
        func = FunctionDict.get(self.ttype.upper())
        if func:
            self.function = func(self.parser, self.node_list)
        else:
            raise SyntaxException("当前函数不存在")
        self.rtype = self.function.rtype
        self.dtype = self.function.dtype

    def __str__(self):
        return str(self.function)


class calcParser():
    def __init__(self, lexer, **kwargs):
        self.lexer = lexer()
        self.parser = yacc.yacc(module=self, write_tables=False)
        self.codes = list()
        self.value_groups = ValueGroup()

    @property
    def tokens(self):
        return self.lexer.tokens

    def p_commands(self, p):
        '''commands : empty
            | command
            | value_groups
        '''
        p[0] = Result(p[1], self.codes)

    def p_command(self, p):
        '''command : node
        '''
        p[0] = Command(self, p[1])

    def p_value_groups(self, p):
        '''value_groups : group
            | value_groups group
        '''
        if len(p) == 2:
            self.value_groups.append(p[1])
            p[0] = self.value_groups
        elif len(p) == 3:
            self.value_groups.append(p[2])
            p[0] = self.value_groups

    def p_group(self, p):
        '''group : node GOTO node
        '''
        if len(p) == 4:
            p[0] = Group(p[1], p[3])

    def p_node_list(self, p):
        '''node_list : node
            | node_list COMMA node
        '''
        if len(p) == 2:
            p[0] = NodeList(p[1])
        elif len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]

    def p_node(self, p):
        '''node : WORD LPAREN node_list RPAREN
            | number
            | string
            | column
            | node PLUS node
            | node MINUS node
            | node TIMES node
            | node DIVIDE node
            | node EQUAL node
            | node GT node
            | node GTE node
            | node LT node
            | node LTE node
            | node OR node
            | node AND node
            | LPAREN node RPAREN
        '''
        if len(p) == 5:
            p[0] = Aggregate(self, p[1], p[3])
        elif len(p) == 4:
            if p[1] == "(" and p[3] == ")":
                p[0] = CalcFirst(p[2])
            elif p[2] == "|":
                p[0] = Part(ttype="|", children=[p[1], p[3]])
            elif p[2] == "&":
                p[0] = Part(ttype="&", children=[p[1], p[3]])
            elif p[2] in (">", ">=", "<", "<=", "=="):
                p[0] = Filter(p[2], p[1], _format_value(p[3]))
            elif p[2] in ("+", "-", "*", "/"):
                p[0] = Calc(p[2], p[1], p[3])
            else:
                raise SyntaxException("不支持的计算符号")
        elif len(p) == 2:
            p[0] = p[1]
        else:
            raise SyntaxException()

    def p_string(self, p):
        'string : STRING'
        p[0] = String(p[1])

    def p_number(self, p):
        '''number : NUMBER
            | MINUS NUMBER
        '''
        if len(p) == 2:
            p[0] = Number(p[1])
        elif len(p) == 3:
            p[0] = Number(f"-{p[2]}")

    def p_column(self, p):
        'column : COLUMN_ID'
        if len(p) == 2:
            column_id = p[1][2:-2]
            column = self.data.get(column_id)
            p[0] = Column(column)

    # Error rule for syntax errors
    def p_error(self, p):
        raise Exception("")

    def p_empty(self, p):
        'empty :'
        pass

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
    )

    def parse(self, string, data=None, show_lexer=False):
        self.data = data
        if show_lexer:
            print("{code}lexer{code}".format(code="=" * 20))
            self.lexer.test(string)
            self.lexer.report()

        # print("{code}parser{code}".format(code="=" * 20))
        return self.parser.parse(string, lexer=self.lexer.lexer)


def get_parser():
    return calcParser(calcLexer)


parser = get_parser()

if __name__ == "__main__":
    import pandas as pd

    options = {
        'display': {
            'max_columns': None,
            'max_colwidth': 25,
            'expand_frame_repr': False,  # Don't wrap to multiple pages
            'max_rows': None,
            'max_seq_items': 50,  # Max length of printed sequence
            'precision': 4,
            'show_dimensions': False
        },
        'mode': {
            'chained_assignment': None  # Controls SettingWithCopyWarning
        }
    }

    for category, option in options.items():
        for op, value in option.items():
            pd.set_option('{category}.{op}'.format(category=category, op=op), value)
            
    s1 = u"""
        {{123456789012345678901234}} == 1  =>  "1分"
        ({{123456789012345678901234}} == 2) | {{123456789012345678901234}} == 3 =>  "2分"
    """

    s2 = u'''
        MEANIF({{5c99f688c3320176fc0bd829}}, ({{123456789012345678901234}} == 2) | ({{223456789012345678901234}} == 3) | ({{323456789012345678901234}} == 3))
    '''

    s3 = u'''
        (MEAN({{5c99f688c3320176fc0bd829}}))*0.6 + (MEAN({{5c99f688c3320176fc0bd829}}))*0.3 + (MEAN({{5c99f688c3320176fc0bd829}}))*0.1
    '''

    s4 = u'''
        (MEAN({{5c99f688c3320176fc0bd829}}))*0.6 + {{5c99f688c3320176fc0bd829}} + (MEAN({{5c99f688c3320176fc0bd829}}))*0.1
    '''

    s5 = u'''
        REPEAT(REVERSE(LOWER(UPPER({{5c99f688c3320176fc0bd831}}))), 2)
    '''

    s6 = '''
        MONTH(DATESUB(DATEADD({{5c99f688c3320176fc0bd830}}, 1), 1))
    '''

    s7 = '''
        GREATEST({{123456789012345678901234}}, {{223456789012345678901234}}, {{323456789012345678901234}}, 7)
    '''

    s8 = '''
        DATEDIFF({{5c99f688c3320176fc0bd830}}, {{5c99f688c3320176fc0bd830}})
    '''

    data = {
        "5d560f9ec332014424ecfc3f": ObjectDict(
            col="城市",
            realcol="城市",
            id="5d560f9ec332014424ecfc3f",
            dtype=model_enums.COLUMN_DTYPE_STRING,
        ),
        "5c99f688c3320176fc0bd829": ObjectDict(
            col="统计数值",
            realcol="统计数值",
            id="5c99f688c3320176fc0bd829",
            dtype=model_enums.COLUMN_DTYPE_INT,
        ),
        "123456789012345678901234": ObjectDict(
            col="NPS1",
            realcol="NPS1",
            id="123456789012345678901234",
            dtype=model_enums.COLUMN_DTYPE_INT,
        ),
        "223456789012345678901234": ObjectDict(
            col="NPS2",
            realcol="NPS2",
            id="223456789012345678901234",
            dtype=model_enums.COLUMN_DTYPE_INT,
        ),
        "323456789012345678901234": ObjectDict(
            col="NPS3",
            realcol="NPS3",
            id="323456789012345678901234",
            dtype=model_enums.COLUMN_DTYPE_INT,
        ),
        "5c99f688c3320176fc0bd831": ObjectDict(
            col="alpha",
            realcol="alpha",
            id="5c99f688c3320176fc0bd831",
            dtype=model_enums.COLUMN_DTYPE_STRING,
        ),
        "5c99f688c3320176fc0bd830": ObjectDict(
            col="time",
            realcol="time",
            id="5c99f688c3320176fc0bd830",
            dtype=model_enums.COLUMN_DTYPE_DATETIME,
        ),
    }

    df = pd.DataFrame({
        "城市": [
            "北京", "天津", "上海", "广州", "浙江", "宁夏", "江苏", "江西", "湖南", 
            "湖北", "河南", "河北", "山东", "黑龙江", "山西", "陕西", "新疆", "云南", "海南", "台湾", 
        ],
        "统计数值": [
            6550034, 634334, 2787768, 674100, 44260, 5350, 72190, 4360, 5489, 34555, 7422, 2611, 
            4544, 5365, 34542, 19131, 8712, 4659, 6587, 56666, 
        ],
        "NPS1": [10, 3, 8, 3, 6, 0, 1, 7, 9, 5, 0, 9, 2, 9, 3, 7, 8, 9, 1, 0, ],
        "NPS2": [10, 10, 9, 10, 6, 0, 0, 3, 2, 5, 1, 10, 4, 5, 2, 10, 0, 3, 0, 8, ],
        "NPS3": [4, 4, 7, 5, 2, 3, 4, 2, 9, 7, 0, 2, 3, 5, 1, 6, 4, 6, 5, 5, ],
        "alpha": [
            "ab", "bc", "cd", "de", "ef", "fg", "gh", "hi", "ij", "jk", "kl", "lm", 
            "mn", "no", "op", "pq", "qr", "rs", "st", "tu"
        ],
        "time": [
            "2019/6/23", "2019/4/11", "2019/2/9", "2019/8/27", "2019/8/16", "2019/3/2", "2019/9/17", 
            "2019/3/26", "2019/1/5", "2019/1/26", "2019/8/31", "2019/8/15", "2019/9/20", "2019/3/4", 
            "2019/7/22", "2019/5/22", "2019/11/9", "2019/1/8", "2019/6/28", "2019/9/21", 
        ],
    })
    df["time"] = pd.to_datetime(df["time"])

    def parse(s):
        try:
            p = calcParser(calcLexer)
            expression = p.parse(s, data=data, show_lexer=True)
            result = expression.result
            print("=" * 40)
            for code in p.codes:
                print(code[1])
                try:
                    df[code[0]] = eval(code[1])
                except Exception as e:
                    print(e)
            print("-" * 40)
            print(result)
            if isinstance(result, ValueGroup):
                column_id = str(uuid.uuid4())
                for group in result:
                    try:
                        df.loc[eval(f"{group.expression}"), column_id] = group.value
                    except Exception as e:
                        print(e)
            else:
                try:
                    print(eval(str(result)))
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    # parse(s1)
    # parse(s2)
    # parse(s3)

    parse(s5)
    print(df)
