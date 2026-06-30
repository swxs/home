# mysqlengine

## Purpose

异步 SQLAlchemy 封装层：提供引擎、会话、声明式 Base、公共 ORM 基类 baseModel、自定义字段类型与通用 Repository，供业务层做异步 CRUD 与分页查询。

## Structure

| 路径                   | 说明                                                                                                                               |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `__init__.py`          | 创建异步 engine、SessionLocal、Declarative Base；定义 baseModel（含 created_at/updated_at 等），导出 Base、SessionLocal、baseModel |
| `fields/`              | 自定义列类型：ObjectIdType、IntEnumField 等                                                                                        |
| `repositories/base.py` | BaseRepository[T]：通用 find_one、search、分页（与 web.schemas.pagination 配合）、search_with_name_like 等                         |

## Key Conventions

- 业务 ORM 模型继承 `mysqlengine.baseModel`，不直接继承 Base。
- 会话通过 `web.dependencies.get_db` 注入；Repository 继承 `BaseRepository[Model]`，由 service 在构造函数显式持有（`self.repo = XxxRepository(db)`），写路径事务边界由 service 的 `async with transaction(self.db):` 统一管理（repo 只 flush、不 commit）。
- Repository 与 `web.schemas.pagination.PageSchema`、业务 schema 配合做搜索与分页。

## Depends On

- `core.config`（MYSQL_URL、池大小等）

## Used By

web（dependencies 中 get_db、transaction 使用 SessionLocal 与 baseModel）、apps 各子应用的 repositories 与 services。
