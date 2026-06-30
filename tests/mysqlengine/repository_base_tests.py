# -*- coding: utf-8 -*-
# @File    : tests/mysqlengine/repository_base_tests.py
# @AUTH    : code_creater

"""BaseRepository 四段原语单测（不连接数据库）。

- _apply_ordering / _apply_filters：直接编译为 SQL 字符串断言，验证白名单与 `-` 降序；
- paginate：用假 session 验证 scalars / Row 两种返回与分页装配。
覆盖历史 bug：`-` 前缀降序此前被静默丢弃。
"""

# 本文件刻意直接测试 BaseRepository 的内部原语；func.count 为 pylint 误报。
# pylint: disable=protected-access,not-callable

import unittest

from sqlalchemy import String, func, select
from sqlalchemy.orm import Mapped, mapped_column

from mysqlengine import baseModel
from mysqlengine.repositories import BaseRepository
from web.schemas.pagination import PageSchema


class _FooModel(baseModel):
    __tablename__ = "_repo_primitive_test_foo"

    name: Mapped[str] = mapped_column(String(50))
    secret: Mapped[str] = mapped_column(String(50))


class _FooRepo(BaseRepository[_FooModel]):
    model = _FooModel
    filterable_fields = {"name"}
    sortable_fields = {"id", "name"}


class _NoWhitelistRepo(BaseRepository[_FooModel]):
    model = _FooModel
    # filterable_fields / sortable_fields 保持默认 None => 拒绝过滤/排序


class _FakeResult:
    def __init__(self, *, scalar=None, items=None):
        self._scalar = scalar
        self._items = items if items is not None else []

    def scalar(self):
        return self._scalar

    def scalars(self):
        return self

    def all(self):
        return self._items


class _FakeDB:
    """按 execute 调用顺序返回预设结果。"""

    def __init__(self, results):
        self._results = list(results)
        self._i = 0
        self.executed = []

    async def execute(self, stmt):
        self.executed.append(str(stmt))
        result = self._results[self._i]
        self._i += 1
        return result


def _sql(query) -> str:
    return str(query)


class ApplyOrderingTestCase(unittest.TestCase):
    def setUp(self):
        self.repo = _FooRepo(None)

    def test_ordering_desc_prefix(self):
        """`-` 前缀应生成 DESC（历史 bug：此前被静默丢弃）。"""
        query = self.repo._apply_ordering(select(_FooModel), PageSchema(order_by=["-name"]))
        sql = _sql(query)
        self.assertIn("ORDER BY", sql)
        self.assertIn("name DESC", sql)

    def test_ordering_ascending_default(self):
        query = self.repo._apply_ordering(select(_FooModel), PageSchema(order_by=["name"]))
        sql = _sql(query)
        self.assertIn("ORDER BY", sql)
        self.assertIn("name ASC", sql)
        self.assertNotIn("DESC", sql)

    def test_ordering_rejects_non_whitelisted_field(self):
        query = self.repo._apply_ordering(select(_FooModel), PageSchema(order_by=["-secret"]))
        self.assertNotIn("ORDER BY", _sql(query))

    def test_ordering_rejected_when_no_whitelist(self):
        repo = _NoWhitelistRepo(None)
        query = repo._apply_ordering(select(_FooModel), PageSchema(order_by=["-name"]))
        self.assertNotIn("ORDER BY", _sql(query))


class ApplyFiltersTestCase(unittest.TestCase):
    def setUp(self):
        self.repo = _FooRepo(None)

    def test_filters_only_whitelisted_field(self):
        query, count_query = self.repo._apply_filters(
            select(_FooModel),
            select(func.count()).select_from(_FooModel),
            {"name": "x", "secret": "y"},
        )
        sql = _sql(query)
        self.assertIn("WHERE", sql)
        self.assertIn("name = ", sql)
        # 非白名单字段 secret 不应进入过滤条件
        self.assertNotIn("secret = ", sql)
        # count_query 同步加上过滤
        self.assertIn("WHERE", _sql(count_query))

    def test_filters_rejected_when_no_whitelist(self):
        repo = _NoWhitelistRepo(None)
        query, count_query = repo._apply_filters(
            select(_FooModel),
            select(func.count()).select_from(_FooModel),
            {"name": "x"},
        )
        self.assertNotIn("WHERE", _sql(query))
        self.assertNotIn("WHERE", _sql(count_query))


class PaginateTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_paginate_scalars_true(self):
        rows = ["a", "b", "c"]
        repo = _FooRepo(_FakeDB([_FakeResult(scalar=7), _FakeResult(items=rows)]))
        out = await repo.paginate(
            select(_FooModel),
            select(func.count()).select_from(_FooModel),
            PageSchema(limit=10, skip=0, page=1, page_number=10),
        )
        self.assertEqual(out["data"], rows)
        self.assertEqual(out["pagination"].total, 7)
        self.assertTrue(out["pagination"].use_pager)

    async def test_paginate_scalars_false_returns_rows(self):
        rows = [("u1", "p1"), ("u2", "p2")]
        repo = _FooRepo(_FakeDB([_FakeResult(scalar=2), _FakeResult(items=rows)]))
        out = await repo.paginate(
            select(_FooModel),
            select(func.count()).select_from(_FooModel),
            PageSchema(limit=10, skip=0, page=1, page_number=10),
            scalars=False,
        )
        self.assertEqual(out["data"], rows)
        self.assertEqual(out["pagination"].total, 2)

    async def test_paginate_zero_total(self):
        repo = _FooRepo(_FakeDB([_FakeResult(scalar=None), _FakeResult(items=[])]))
        out = await repo.paginate(
            select(_FooModel),
            select(func.count()).select_from(_FooModel),
            PageSchema(),
        )
        self.assertEqual(out["data"], [])
        self.assertEqual(out["pagination"].total, 0)


if __name__ == "__main__":
    unittest.main()
