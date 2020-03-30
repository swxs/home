# -*- coding: utf-8 -*-
# @File    : helper_keywords_tests.py
# @AUTH    : swxs
# @Time    : 2018/11/12 18:17

import unittest
from common.Helpers.Helper_keywords import Trie


class KeywordsHelperTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 假设危险词列表
        q_keywords_list = ['蚂蚁', '老鼠', '苍蝇', '小强']
        # 生成危险词树
        cls.trie = Trie(keywords_list=q_keywords_list)

    def test_keywords(self):
        # 要检测的文本内容
        content = '有小强，米老鼠玩偶很可爱aaa'
        keywords, keywords_position = KeywordsHelperTestCase.trie.match_all(content)
        self.assertEqual(keywords, ['小强', '老鼠'])
        self.assertEqual(keywords_position, [1, 5])

    def test_keywords_multi(self):
        # 要检测的文本内容
        content = '有小强，郑小强。老鼠爱大米主题很有意思,米老鼠玩偶很可爱aaa'
        keywords, keywords_position = KeywordsHelperTestCase.trie.match_all(content)
        self.assertEqual(keywords, ['小强', '小强', '老鼠', '老鼠'])
        self.assertEqual(keywords_position, [1, 5, 8, 21])


class ReverseKeywordsHelperTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 假设危险词列表
        q_keywords_list = ['蚂蚁', '老鼠', '苍蝇', '小强']

        # 假设危险词反词表列表
        reversedwords_dict = {
            '老鼠': ['米老鼠']
        }

        # 生成危险词树
        cls.trie = Trie(keywords_list=q_keywords_list, reversedwords_dict=reversedwords_dict)

    def test_reverse_keywords(self):
        content = '有小强，郑小强。老鼠爱大米主题很有意思,米老鼠玩偶很可爱'
        keywords, keywords_position = (ReverseKeywordsHelperTestCase.trie.match_all(content))

        self.assertEqual(keywords, ['小强', '小强', '老鼠'])
        self.assertEqual(keywords_position, [1, 5, 8])
