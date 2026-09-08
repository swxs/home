# -*- coding: utf-8 -*-
# @File    : tests/apps/repository_migration_tests.py
# @AUTH    : code_creater

"""迁移到基类原语后的 3 个自定义 repo 回归测试（用假 session，不连接数据库）。

验证：
- password_lock.search_with_name_like：等值过滤 + name/website 模糊搜索 + 分页装配；
- sudoku_completion.search_by_user_with_puzzle_filter：join 返回 Row、缺省按完成时间倒序；
- user_search.search_with_auth：单条 SQL 内联相关聚合拍平 phone/email，并重塑为 (User, {...})。
"""

import unittest

from home.apps.password_lock.repositories.password_lock_repository import PasswordLockRepository
from home.apps.password_lock.schemas.password_lock import PasswordLockFilter
from home.apps.sudoku.repositories.sudoku_completion_repository import SudokuCompletionRepository
from home.apps.system.repositories.user_search_repository import UserSearchRepository
from home.apps.system.schemas.user import UserFilter
from home.web.schemas.pagination import PageSchema


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
    """按 execute 调用顺序返回预设结果，并记录被执行语句的字符串形式。"""

    def __init__(self, results):
        self._results = list(results)
        self._i = 0
        self.executed = []

    async def execute(self, stmt):
        self.executed.append(str(stmt))
        result = self._results[self._i]
        self._i += 1
        return result


class _FakeRow:
    """模拟 SQLAlchemy Row：支持 row[0] 与 row._mapping[name]。"""

    def __init__(self, obj, mapping):
        self._obj = obj
        self._mapping = mapping

    def __getitem__(self, idx):
        if idx == 0:
            return self._obj
        raise IndexError(idx)


class PasswordLockSearchTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_filter_plus_fuzzy_search(self):
        repo = PasswordLockRepository(_FakeDB([_FakeResult(scalar=2), _FakeResult(items=["pl1", "pl2"])]))
        out = await repo.search_with_name_like(
            PasswordLockFilter(user_id="a" * 24),
            PageSchema(),
            name_search="git",
        )
        self.assertEqual(out["data"], ["pl1", "pl2"])
        self.assertEqual(out["pagination"].total, 2)

        data_sql = repo.session.executed[1].lower()
        self.assertIn("like", data_sql)          # name/website 模糊搜索
        self.assertIn("user_id", data_sql)        # 白名单等值过滤


class SudokuCompletionSearchTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_returns_rows_default_desc(self):
        repo = SudokuCompletionRepository(_FakeDB([_FakeResult(scalar=1), _FakeResult(items=[("c", "p")])]))
        out = await repo.search_by_user_with_puzzle_filter(user_id="u1", page_schema=PageSchema())

        # returns_scalars=False => 返回 (Completion, Puzzle) 行
        self.assertEqual(out["data"], [("c", "p")])
        self.assertEqual(out["pagination"].total, 1)

        data_sql = repo.session.executed[1]
        self.assertIn("ORDER BY", data_sql)
        self.assertIn("DESC", data_sql)           # 缺省 completed_at 倒序


class UserSearchFlattenTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_single_query_flatten(self):
        user = object()
        row = _FakeRow(user, {"phone": "13800000000", "email": "x@e.com"})
        repo = UserSearchRepository(_FakeDB([_FakeResult(scalar=1), _FakeResult(items=[row])]))

        rows, pagination = await repo.search_with_auth(UserFilter(), PageSchema())

        self.assertEqual(rows, [(user, {"phone": "13800000000", "email": "x@e.com"})])
        self.assertEqual(pagination.total, 1)

        data_sql = repo.session.executed[1].lower()
        # 相关聚合子查询把认证 identifier 拍平为列
        self.assertIn("max(user_auth.identifier)", data_sql)


if __name__ == "__main__":
    unittest.main()
