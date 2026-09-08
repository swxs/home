# web

## Purpose

HTTP 层：统一异常体系、依赖注入（数据库会话、事务上下文）、通用请求/响应 schema（分页、搜索、token）、全局异常处理与中间件，供 apps 复用。

## Structure

| 路径              | 说明                                                                                                                                                                                           |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `exceptions/`     | BaseHttpException（status_code, code, message, data）；4xx/5xx 子类（如 Http400BadRequestException、Http404NotFoundException、Http422UnprocessableEntityException 等），每类含类属性错误码常量 |
| `dependencies/`   | `session.py`：`get_session`（HTTP 请求级 session 依赖）、`transaction`（写路径薄封装，含 DB→HTTP 异常转换）                                                                                      |
| `handlers/`       | unknown_http_handler、unknown_exception_handler，在 main.py 中注册给 FastAPI                                                                                                                   |
| `middlewares/`    | 中间件                                                                                                                                                                                         |
| `schemas/`        | pagination、response、search、token；`types/`（Pydantic 复用类型，如 `objectId`）                                                                                                              |
| `response.py`     | 统一响应构造（如 success、exception）                                                                                                                                                          |

## Key Conventions

- 业务层通过 `from home.web.exceptions import ...` 抛出 HTTP 异常；异常码格式为 `status_code * 1000 + 序号`（如 400001）。
- service 通过依赖工厂 `get_xxx_service(session=Depends(get_session))` 拿到会话；写路径用 `async with transaction(self.session):` 包裹（见 `web/dependencies/session.py`）。
- 分页/搜索/token 通过 `Depends(get_pagination)`、`Depends(get_search)`、`Depends(get_token)` 注入。
- Path/Query 中的 ObjectId 使用 `objectId` 类型，见 [docs/conventions/types.md](../../../docs/conventions/types.md)。

## Depends On

core、mysqlengine（open_session、transaction、baseModel、BaseRepository）。

## Used By

apps 下各子应用的 api、services、repositories 等。
