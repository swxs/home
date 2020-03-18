# -*- coding: utf-8 -*-
# @File    : ExpressionParser.py
# @AUTH    : swxs
# @Time    : 2018/8/24 17:11

import re
import asyncio
import datetime
from functools import partial
from itertools import count
from apps.errors import AppResourceError
from exceptions import *
from commons.log_utils import get_logging
from commons.Helpers.Helper_validate import Validate, RegType
from apps.bi import model_enums
from .parser_exception import SyntaxException


logger = get_logging("ExpressionParser")


class Node():
    def __init__(self, deep=0):
        self.stack = []
        self.deep = deep
        self.next = None
        self.prev = None
    
    def add_child(self, node):
        self.next = node
        node.prev = self

    def append(self, value):
        self.stack.append(value)

    def __repr__(self):
        return f"stack: {self.stack}, deep: {self.deep}, prev: {self.prev!r}"

class ExpressionCompiler(object):
    R1 = re.compile(r'\[\s*([^\]]+)\s*\]')

    def __init__(self, expression, ttype, worktable_id):
        self.expression = expression
        self.ttype = ttype
        self.dtype = None
        self.worktable_id = worktable_id
        self._expression = None
        self._expression_column_id_list = []
        self._value_group_list = []

    async def get_compile_expression(self):
        if not self._expression:
            if self.ttype == model_enums.COLUMN_TTYPE_GROUP:
                self._value_group_list = await self.split_expression(self.expression)
                self._expression, self._expression_column_id_list, parsed_expression = await ExpressionCompiler.compile_value_expression(self.expression, self.worktable_id)
            else:
                self._expression, self._expression_column_id_list, parsed_expression = await ExpressionCompiler.compile_and_check_expression(self.expression, self.worktable_id)
                parsed_result_rtype = parsed_expression.result.rtype
                parsed_result_dtype = parsed_expression.result.dtype
                if parsed_result_rtype == "AGG":
                    self.ttype = model_enums.COLUMN_TTYPE_CALC
                    self.dtype = model_enums.COLUMN_DTYPE_CALC
                elif parsed_result_rtype in ("RAW", "COLUMN", "SERIES"):
                    self.ttype = model_enums.COLUMN_TTYPE_CHANGE
                    if parsed_result_dtype == "NUMBER":
                        self.dtype = model_enums.COLUMN_DTYPE_INT
                    elif parsed_result_dtype == "STRING":
                        self.dtype = model_enums.COLUMN_DTYPE_STRING
                    elif parsed_result_dtype == "DATETIME":
                        self.dtype = model_enums.COLUMN_DTYPE_DATETIME
                    else:
                        pass
        return self._expression

    async def split_expression(self, expression):
        value_group_list = []
        expression_string_list = expression.split("\n")
        for expression_string in expression_string_list:
            if expression_string == "":
                continue
            elif "=>" in expression_string:
                expression, name = expression_string.split("=>")
                compiled_expression, expression_column_id_list, parsed_expression = await ExpressionCompiler.compile_and_check_value_expression(expression, name, self.worktable_id)
                value_group_list.append(dict(name=name.strip(), expression=compiled_expression, expression_column_id_list=expression_column_id_list))
            else:
                continue
        return value_group_list

    def get_expression_column_id_list(self):
        return self._expression_column_id_list

    def get_expression_ttype(self):
        return self.ttype

    def get_expression_dtype(self):
        if self.ttype == model_enums.COLUMN_TTYPE_CALC:
            return model_enums.COLUMN_DTYPE_INT
        elif self.ttype == model_enums.COLUMN_TTYPE_CHANGE:
            if self.dtype:
                return self.dtype
            else:
                return model_enums.COLUMN_DTYPE_INT
        elif self.ttype == model_enums.COLUMN_TTYPE_GROUP:
            for value_group in self._value_group_list:
                if not Validate.check(value_group.get('name'), RegType.NUMBER):
                    return model_enums.COLUMN_DTYPE_STRING
            return model_enums.COLUMN_DTYPE_INT
        else:
            return model_enums.COLUMN_DTYPE_STRING

    @staticmethod
    def compile_expression(expression, column_list):
        node = Node(deep=0)
        current_node = node
        for exp in expression:
            if exp == "[":
                new_node = Node(deep=current_node.deep + 1)
                current_node.add_child(new_node)
                current_node = new_node
            elif exp == "]":
                if current_node.deep == 1:
                    maybe_column_col = "".join(current_node.stack)

                    current_column = None
                    for column in column_list:
                        if column.readablecol == maybe_column_col:
                            current_column = column
                            break

                    if current_column:
                        node_part = f"{{{{{current_column.id}}}}}"  # convert readable_col to {{column_id}}
                    else:
                        node_part = f"[{maybe_column_col}]"
                    
                    old_current_node = current_node
                    current_node = old_current_node.prev
                    current_node.append(node_part)
                elif current_node.deep == 0:
                    raise Exception
                else:
                    node_part = f"[{''.join(current_node.stack)}]"
                    old_current_node = current_node
                    current_node = old_current_node.prev
                    current_node.append(node_part)
            else:
                current_node.append(exp)

        if current_node.deep == 0:
            return "".join(current_node.stack)
        else:
            raise Exception

    @staticmethod
    async def compile_value_expression(expression, worktable_id):
        from apps.bi import column_utils
        column_list = await column_utils.get_column_list_by_worktable_id(worktable_id)
        changed_readablecol_expression = ExpressionCompiler.compile_expression(expression, column_list)
        changed_index_expression, expression_column_id_list = ExpressionParser.split_expression(changed_readablecol_expression)
        return changed_index_expression, expression_column_id_list, {}

    @staticmethod
    async def compile_and_check_expression(expression, worktable_id):
        from apps.bi import column_utils
        column_list = await column_utils.get_column_list_by_worktable_id(worktable_id)
        changed_readablecol_expression = ExpressionCompiler.compile_expression(expression, column_list)
        changed_index_expression, expression_column_id_list = ExpressionParser.split_expression(changed_readablecol_expression)
        # 下面判断是否合法
        try:
            parsed_expression = await ExpressionParser.code_format_to_col(changed_index_expression, expression_column_id_list, worktable_id)
        except SyntaxException as e:
            raise ResourceError(AppResourceError.InvalidFormat, f"{e}")
        except Exception:
            raise ResourceError(AppResourceError.InvalidFormat, "计算字段格式不正确！")
        return changed_index_expression, expression_column_id_list, parsed_expression

    @staticmethod
    async def compile_and_check_value_expression(expression, name, worktable_id):
        from apps.bi import column_utils
        column_list = await column_utils.get_column_list_by_worktable_id(worktable_id)
        changed_readablecol_expression = ExpressionCompiler.compile_expression(expression, column_list)
        changed_index_expression, expression_column_id_list = ExpressionParser.split_expression(changed_readablecol_expression)
        # 下面判断是否合法
        try:
            parsed_expression = await ExpressionParser.code_format_to_col(f"{changed_index_expression} => {name}", expression_column_id_list, worktable_id)
        except Exception:
            raise ResourceError(AppResourceError.InvalidFormat, "分组字段格式不正确！")
        return changed_index_expression, expression_column_id_list, parsed_expression


class ExpressionParser():
    R1 = re.compile(r'\{\{([0-9a-zA-Z]{24})\}\}')
    R2 = re.compile(r'\{\{(\d+)\}\}')

    @staticmethod
    def split_expression(expression):
        counter = count(0)
        column_id_list = []

        def compiler(x):
            column_id = ExpressionParser.R1.findall(x.group(0))[0]
            if column_id:
                column_id_list.append(column_id)
                return f"{{{{{next(counter)}}}}}"  # {{index}}
            else:
                return x.group(0)

        real_expression = ExpressionParser.R1.sub(compiler, expression)
        return real_expression, column_id_list

    @staticmethod
    def combine_expression(expression, expression_column_id_list, calc_column_expression_dict=None):
        if calc_column_expression_dict is None:
            calc_column_expression_dict = {}

        def compiler(x):
            column_id_index = ExpressionParser.R2.findall(x.group(0))[0]
            column_id = expression_column_id_list[int(column_id_index)]

            if column_id:
                if column_id in calc_column_expression_dict:
                    return f"{calc_column_expression_dict[column_id]}"
                else:
                    return f"{{{{{str(column_id)}}}}}"
            else:
                return x.group(0)

        return ExpressionParser.R2.sub(compiler, expression)

    @staticmethod
    async def code_format_to_col(expression, expression_column_id_list, worktable_id):
        from apps.bi import column_utils
        from apps.bi import worktable_utils

        worktable = await worktable_utils.get_worktable(worktable_id)

        column_dict = await worktable_utils.get_column_dict(worktable)

        calc_column_expression_dict = dict()
        for expression_column_id in expression_column_id_list:
            expression_column = await column_utils.get_column(expression_column_id)
            if expression_column.ttype in (model_enums.COLUMN_TTYPE_CALC, model_enums.COLUMN_TTYPE_CHANGE):
                calc_column_expression_dict[expression_column_id] = await column_utils.get_real_expression(expression_column)

        parser = worktable_utils.get_parser(worktable)
        real_expression = ExpressionParser.combine_expression(
            expression,
            expression_column_id_list,
            calc_column_expression_dict=calc_column_expression_dict,
        )
        logger.info(f"real_expression: {real_expression}")
        return parser.parse(real_expression, data=column_dict)

    @staticmethod
    async def code_format_to_readable_col(expression, expression_column_id_list):
        from apps.bi import column_utils
        expression_column_list = []
        for expression_column_id in expression_column_id_list:
            expression_column = await column_utils.get_column(expression_column_id)
            expression_column_list.append(expression_column)

        def compiler(x):
            column_id_index = ExpressionParser.R2.findall(x.group(0))[0]
            column = expression_column_list[int(column_id_index)]
            if column:
                return f'[{column.readablecol}]'
            else:
                return x.group(0)

        return ExpressionParser.R2.sub(compiler, expression)
