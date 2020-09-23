#!usr/bin/env python
# -*- coding:utf-8 _*-
# @author:fang
# @file: Helper_keywords.py
# @time: 2018/9/9/14:16
# @Software: PyCharm
# @Describe:

import re

from collections import defaultdict


class TrieNode(object):
    """
    Trie 节点.
    """

    def __init__(self):
        self.val = None
        self.trans = {}


class ReversedWordNode(object):
    """
    ReversedWord 反危险词
    """

    def __init__(self, start, length, reversedwords):
        self.start = start
        self.length = length
        self.reversedwords = reversedwords


class Trie(object):
    """
    Trie: 实现脏词索引数据的生成, 以及提供脏词检测.
    为了减少Trie树的深度, 使用unicode字符编码构建, 而不使用'utf-8'编码.
    """

    def __init__(self, keywords_list=None, reversedwords_dict=None):
        # 初始化Trie树的根节点.
        self.root = TrieNode()
        self.word_set = set()
        self.reversedwords_dict = defaultdict(list)

        if keywords_list:
            self.add_keywords_list(keywords_list)
        if reversedwords_dict:
            self.add_reversedwords_dict_dict(reversedwords_dict)

    def add(self, word):
        """
        生成 Trie 字典树.
        @return: 暂无.
        @param word[type unicode]: 单个脏词, 必须是 unicode 类型.
        """
        curr_node = self.root
        for ch in word:
            tmp_node = curr_node.trans.get(ch)
            if tmp_node is None:
                curr_node.trans[ch] = TrieNode()
                curr_node = curr_node.trans[ch]
            else:
                curr_node = tmp_node

        curr_node.val = word
        self.word_set.add(word)

    def add_keywords_list(self, keywords_list):
        for word in keywords_list:
            self.add(word)

    def add_reversedwords_dict_dict(self, reversedwords_dict):
        for keywords, reversedwords_list in reversedwords_dict.items():
            for reversedwords in reversedwords_list:
                for group in re.finditer(rf'.*?(?P<keyword>{keywords})', reversedwords, re.M):
                    self.reversedwords_dict[keywords].append(
                        ReversedWordNode(group.start("keyword"), length=len(reversedwords), reversedwords=reversedwords)
                    )

    def __walk(self, trie_node, ch):
        """
        检查当前节点中是否包含 unicode 字符.

        @return: 如果匹配, 返回 unicode 字符对应的节点.
            否则, 返回 None.
        """

        if ch in trie_node.trans:
            trie_node = trie_node.trans.get(ch)
            return trie_node

        return None

    def __find_ch(self, sub_content):
        """
        从 sub_content 中筛选出脏词.

        @return: 被命中的脏词.
        @rtype: list.
        @param sub_content[unicode]: 待检测内容.
        """
        words = []
        limit = len(sub_content)
        curr_node = self.root

        for start in range(limit):
            ch = sub_content[start]

            curr_node = self.__walk(curr_node, ch)
            if curr_node is None:
                return words

            if curr_node.val:
                words.append(curr_node.val)

        return words

    def __is_reversedwords(self, content, position, reversedword):
        try:
            return (
                content[position - reversedword.start : position - reversedword.start + reversedword.length]
                == reversedword.reversedwords
            )
        except Exception:
            return False

    def match_all(self, content):
        """
        找出内容中的所有脏词.

        @return: 命中的脏词列表.
        @rtype: list.
        @param content[type unicode]: 待检测的 unicode 字符串.
        """
        keyword_list = []
        keyword_position_list = []
        size = len(content)

        for index in range(size):
            val = self.__find_ch(content[index:size])
            if val:
                keyword_list.extend(val)
                keyword_position_list.append(index)

        return self.clear_reversedwords(content, keyword_list, keyword_position_list)

    def clear_reversedwords(self, content, keyword_list, keyword_position_list):
        cleared_keyword_list = []
        cleared_keyword_position_list = []

        for keyword, position in zip(keyword_list, keyword_position_list):
            is_reversedwords = False
            if keyword in self.reversedwords_dict:
                for reversedword in self.reversedwords_dict[keyword]:
                    is_reversedwords = self.__is_reversedwords(content, position, reversedword)
                    if is_reversedwords:
                        break

            if not is_reversedwords:
                cleared_keyword_list.append(keyword)
                cleared_keyword_position_list.append(position)
        return cleared_keyword_list, cleared_keyword_position_list

    @property
    def words(self):
        return self.word_set
