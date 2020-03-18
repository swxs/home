# -*- coding: utf-8 -*-
# @File    : calc_lexer.py.py
# @AUTH    : swxs
# @Time    : 2018/10/31 16:37

import ply.lex as lex
import ply.yacc as yacc


class calcLexer():
    def __init__(self, **kwargs):
        self.errors = []
        # Build the lexer
        self.lexer = lex.lex(module=self, **kwargs)

    errors = []

    # 保留字
    reserved = {}

    tokens = [
        'STRING', 'COLUMN_ID', 'NUMBER', 'WORD', 
        'GOTO',
        'QUOTE', 'COMMA',
        'OR', 'AND',
        'EQUAL', 'GTE', 'LTE', 'GT', 'LT',
        'LPAREN', 'RPAREN',
        'OBRACE', 'EBRACE',
        'TIMES', 'DIVIDE',
        'PLUS', 'MINUS',
        'SEMICOLON',
    ] + list(set(reserved.values()))

    # t_NUMBER = r'[0-9]+'
    t_STRING = r"\"[^\"]*\""
    t_QUOTE = r'"'
    t_COMMA = r","
    t_OR = r'\|'
    t_AND = r'&'
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_OBRACE = r'{'
    t_EBRACE = r'}'
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_EQUAL = r'=='
    t_GTE = r'>='
    t_LTE = r'<='
    t_GT = r'>'
    t_LT = r'<'
    t_GOTO = r'=>'
    t_SEMICOLON = r';'
    t_COLUMN_ID = t_OBRACE + t_OBRACE + r'[a-z0-9]{24}' + t_EBRACE + t_EBRACE

    # t_AGG_FILTER = r'[*]'

    def t_NUMBER(self, t):
        r'[0-9]+(\.[0-9]+)?'
        return t

    def t_WORD(self, t):
        r'[a-zA-Z0-9\u4e00-\u9fa5]+'
        t.type = calcLexer.reserved.get(t.value, 'WORD')
        return t

    # 不做处理的符号 空格与tab
    t_ignore = " \t"

    # 行号统计
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    # 出错处理
    def t_error(self, t):
        self.errors.append("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def test(self, string):
        self.errors = []
        self.lexer.input(string)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

    def report(self):
        return self.errors
