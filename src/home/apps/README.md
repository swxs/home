# apps

## Purpose

业务应用集合，每个子应用对应一个业务域，路由挂载到 `/api`。在 `apps/__init__.py` 中汇总各子应用 router 到 `api_router`。

## Structure

各子应用采用统一五层分层：

- **api/**：FastAPI 路由（APIRouter），依赖 web（get_db、exceptions、schemas），仅调用 service 并包装响应
- **services/**：业务层，承载业务编排、归属授权、领域规则与事务边界（写路径用 `async with transaction(self.db):`）
- **models/**：ORM 模型（继承 `home.mysqlengine.baseModel`）
- **repositories/**：数据访问，继承或组合 `home.mysqlengine.repositories.BaseRepository`；只 flush、不 commit
- **schemas/**：Pydantic 请求/响应模型与 Depends 用的工厂（如 get_xxx_filter）

> 分层规范详见 [docs/architecture/layering.md](../docs/architecture/layering.md)。

子应用列表：

| 子应用        | 功能                                       |
| ------------- | ------------------------------------------ |
| password_lock | 密码管理                                   |
| sudoku        | 数独题目与完成记录、图片解析               |
| system        | 系统能力、用户等；含 OAuth（oauth_router） |
| upload        | 上传                                       |
| wechat        | 微信相关                                   |

## Key Conventions

- 子应用 router 在 `apps/__init__.py` 中 import 并 `api_router.include_router(router=xxx_router)`。
- 业务层依赖 web（dependencies、exceptions、schemas）和 mysqlengine，不反向依赖其他 app。

## Depends On

web、mysqlengine；部分功能可能使用 commons。

## Used By

main.py 通过 `from home.apps import api_router` 并 `app.include_router(router=api_router)` 挂载。
