# apps

## Purpose

业务应用集合，每个子应用对应一个业务域，路由挂载到 `/api`。在 `apps/__init__.py` 中汇总各子应用 router 到 `api_router`。

## Structure

各子应用采用统一分层：

- **api/**：FastAPI 路由（APIRouter），依赖 web（get_db、get_single_worker、exceptions、schemas）、本 app 的 models/repositories/schemas
- **models/**：ORM 模型（继承 mysqlengine.baseModel）
- **repositories/**：数据访问，继承或组合 mysqlengine.repositories.BaseRepository
- **schemas/**：Pydantic 请求/响应模型与 Depends 用的工厂（如 get_xxx_schema）

子应用列表：

| 子应用        | 功能                                       |
| ------------- | ------------------------------------------ |
| password_lock | 密码管理                                   |
| system        | 系统能力、用户等；含 OAuth（oauth_router） |
| upload        | 上传                                       |
| wechat        | 微信相关                                   |
| workflow      | 工作流（图、技能、运行存储等）             |

## Key Conventions

- 子应用 router 在 `apps/__init__.py` 中 import 并 `api_router.include_router(router=xxx_router)`。
- 业务层依赖 web（dependencies、exceptions、schemas）和 mysqlengine，不反向依赖其他 app。

## Depends On

web、mysqlengine；部分功能可能使用 commons。

## Used By

main.py 通过 `from apps import api_router` 并 `app.include_router(router=api_router)` 挂载。
