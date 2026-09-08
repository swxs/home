# 复用类型约定（types）

本规范定义 `home.web.schemas.types` 下 Pydantic 复用类型的用法，以及与 ORM / SQLAlchemy 层类型的分工。

> 实现位置：`src/home/web/schemas/types/`（当前含 `object_id.py`）。

---

## objectId

MongoDB 风格 ObjectId：24 位十六进制字符串，通过 `bson.ObjectId` 校验（比纯 regex 更严格）。

### Import

```python
from home.web.schemas.types import objectId
```

### 适用场景

| 场景 | 写法 | 说明 |
|------|------|------|
| Path 参数 | `resource_id: objectId = Path(...)` | 替代 `str = Path(..., regex="[0-9a-fA-F]{24}")` |
| Query 参数 | `user_id: Optional[objectId] = Query(None)` | 与 schema 字段一致 |
| Body / Filter schema | `user_id: Optional[objectId] = None` | 继承或组合 `BaseSchema` |
| Token 载荷 | `TokenSchema.user_id: Optional[objectId]` | JWT decode 后由 Pydantic 校验 |
| 必登录 api | `user_id: objectId = Depends(get_required_user_id)` | 保证 user_id 非空 |
| service / repository | `user_id: objectId`、`resource_id: objectId` | 与 schema 类型一致，见 layering.md |
| ORM 字段标注 | `user_id: Mapped[objectId] = mapped_column(ObjectIdType, ...)` | Python 侧类型；列类型用 `ObjectIdType` |

### 禁止

- 在 api / schema 中手写 `regex="[0-9a-fA-F]{24}"` 或等价 pattern 校验 ObjectId
- 为 Path 单独再定义 `Annotated` 别名（除非确有重复 metadata 需求）

### 校验失败

`validate_object_id` 抛出 `ValueError`，由 FastAPI / Pydantic 返回 **422**（请求参数格式错误），不在 service 层转业务 400。

### 与 mysqlengine 的分工

| 层 | 类型 | 职责 |
|----|------|------|
| `web.schemas.types.objectId` | Pydantic `Annotated` | HTTP 入参 / 出参契约校验 |
| `mysqlengine.fields.ObjectIdType` | SQLAlchemy `TypeDecorator` | 数据库存储（binary(12) ↔ hex str） |

ORM model 可同时使用两者：`Mapped[objectId]` + `mapped_column(ObjectIdType)`。

### 示例

```python
# api
@router.get("/{password_lock_id}")
async def get_password_lock(
    password_lock_id: objectId = Path(...),
    service: PasswordLockService = Depends(get_password_lock_service),
):
    ...

# schema
class PasswordLockFilter(BaseSchema):
    user_id: Optional[objectId] = None
```

---

## 扩展新类型

新增复用类型时：

1. 在 `schemas/types/<name>.py` 定义
2. 在 `schemas/types/__init__.py` 导出
3. 在本文件补充适用场景与禁止项
