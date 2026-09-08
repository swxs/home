# -*- coding: utf-8 -*-
# @File    : repositories/__init__.py
# @AUTH    : code_creater

"""system 模块 Repository 分工与使用约定。

分工
- 表级 Repository（继承 ``BaseRepository[Model]``，如 ``UserRepository``、``UserAuthRepository``）：
  负责单表 CRUD 与表内自定义查询。``model`` 以类属性声明，统一构造为 ``Repo(session)``。
- 聚合 Repository（不继承 ``BaseRepository``，如 ``UserSearchRepository``、``UserIdentityRepository``）：
  跨多表取数 / find-or-create，**只返回 ORM 对象**（拼接与 DTO 转换交给 service）；
  仅依赖 session，内部以 ``Repo(session)`` 组合表级 repo。

构造与持有
- repo 由 service 在构造函数里**显式持有**（``self.repo = XxxRepository(session)``），支持可选注入便于单测；
  不再使用 ``SingleWorker`` / ``UnitWorker`` / ``get_repository`` 这类服务定位器写法。

事务边界
- 写路径用 ``async with transaction(self.session):``（见 ``web/dependencies/transaction.py``）统一 commit / rollback；
  只读路径不包事务（同一 session 内多次查询天然一致）。
- 表级 / 聚合 repo 一律**只 flush、不 commit**；事务边界永远在 service。
"""

# 本模块方法
from .user_auth_repository import UserAuthRepository
from .user_identity_repository import UserIdentityRepository
from .user_repository import UserRepository
from .user_search_repository import UserSearchRepository

__all__ = [
    "UserRepository",
    "UserAuthRepository",
    "UserSearchRepository",
    "UserIdentityRepository",
]
