# mysqlengine

## Purpose

异步 SQLAlchemy 封装层：提供引擎、会话、事务原语、声明式 Base、公共 ORM 基类 baseModel、自定义字段类型与通用 Repository，供业务层做异步 CRUD 与分页查询。

## Structure

| 路径                   | 说明                                                                                                                               |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `__init__.py`          | 创建异步 engine、SessionLocal、Declarative Base；定义 baseModel；导出 Base、SessionLocal、baseModel、open_session、transaction      |
| `session.py`           | `open_session()`（创建/关闭 session）、`transaction(session)`（纯 commit/rollback，供脚本与后台任务）                              |
| `fields/`              | 自定义列类型：ObjectIdType、IntEnumField 等                                                                                        |
| `repositories/base.py` | BaseRepository[T]：通用 find_one、search、分页（与 web.schemas.pagination 配合）、search_with_name_like 等                         |

## Key Conventions

- 业务 ORM 模型继承 `home.mysqlengine.baseModel`，不直接继承 Base。
- HTTP 请求内 session 通过 `home.web.dependencies.session.get_session` 注入；非 HTTP 场景（脚本、BackgroundTasks）用 `open_session()`。
- Repository 继承 `BaseRepository[Model]`，由 service 在构造函数显式持有（`self.repo = XxxRepository(session)`）。
- 写路径事务边界：service 用 `async with transaction(self.session):`（HTTP 场景 import 自 `web.dependencies.session`）；脚本/后台 import 自 `home.mysqlengine`。repo 只 flush、不 commit。

## Depends On

- `home.core.config`（MYSQL_URL、池大小等）

## Used By

web（`dependencies/session.py` 薄封装 mysqlengine 原语）、apps 各子应用的 repositories 与 services。
