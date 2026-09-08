# commons

## Purpose

跨应用通用工具：装饰器、Helper、元类、Utils，被 apps 或其它包按需引用，无业务域归属。

## Structure

| 路径        | 说明                                                                      |
| ----------- | ------------------------------------------------------------------------- |
| Decorators/ | 通用装饰器                                                                |
| Helpers/    | 各类辅助函数（如 encoder、validate、keywords、prototype 等），含 Lua 相关 |
| Metaclass/  | 元类（如 singleton）                                                      |
| Utils/      | 工具函数                                                                  |

## Key Conventions

- 纯工具代码，不依赖 web、apps 业务层；可依赖 `home.core`。
- 测试在 `tests/commons/` 下有对应用例（如 Helpers、Metaclass）。

## Used By

apps 或其它模块按需 import；isort 配置中 `known_first_party` 包含 `home`。
