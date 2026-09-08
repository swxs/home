# docs 文档地图

本目录收录 `home` 项目的工程规范与约定文档，按主题分目录组织。新增文档请归入对应主题目录，并在此处登记。

## 场景索引

- 想了解领域术语与概念边界 -> 根目录 [CONTEXT.md](../CONTEXT.md)
- 想了解顶层包结构、子应用与依赖方向 -> [architecture/project-overview.md](architecture/project-overview.md)
- 想了解 app 的五层架构、各层职责、目录结构、数据流与事务边界 -> [architecture/layering.md](architecture/layering.md)
- 想了解 repository 查询层（过滤 / 排序 / 分页 / 自定义查询）的统一写法 -> [conventions/repository.md](conventions/repository.md)
- 想了解 Path/Query/Body 复用类型（如 objectId）-> [conventions/types.md](conventions/types.md)
- 想了解已记录的架构决策 -> [adr/](adr/)

## 目录约定

```
docs/
├── README.md          # 本文件：文档地图与索引
├── adr/               # 架构决策记录（难逆转、有 trade-off 的决策）
├── architecture/      # 架构与分层设计（跨模块的结构性规范）
├── conventions/       # 编码约定与统一写法（可落到具体层/写法）
└── specs/             # 功能规格（按特性）
```

- `adr/`：记录已做出的、难逆转的架构决策；见 [adr/](adr/)。
- `architecture/`：描述系统/模块的结构、分层、职责边界与数据流。
- `conventions/`：描述具体编码约定与统一写法，便于 review 时对齐。
- 领域术语见根目录 [CONTEXT.md](../CONTEXT.md)；顶层包概览见 [architecture/project-overview.md](architecture/project-overview.md)。
