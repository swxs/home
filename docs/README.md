# docs 文档地图

本目录收录 `home` 项目的工程规范与约定文档，按主题分目录组织。新增文档请归入对应主题目录，并在此处登记。

## 场景索引

- 想了解 app 的五层架构、各层职责、目录结构、数据流与事务边界 -> [architecture/layering.md](architecture/layering.md)
- 想了解 repository 查询层（过滤 / 排序 / 分页 / 自定义查询）的统一写法 -> [conventions/repository.md](conventions/repository.md)

## 目录约定

```
docs/
├── README.md          # 本文件：文档地图与索引
├── architecture/      # 架构与分层设计（跨模块的结构性规范）
└── conventions/       # 编码约定与统一写法（可落到具体层/写法）
```

- `architecture/`：描述系统/模块的结构、分层、职责边界与数据流。
- `conventions/`：描述具体编码约定与统一写法，便于 review 时对齐。
- 顶层包（`core` / `web` / `apps` / `mysqlengine` 等）的概览说明仍放在各自目录下的 `README.md`；项目整体上下文见根目录 [CONTEXT.md](../CONTEXT.md)。
