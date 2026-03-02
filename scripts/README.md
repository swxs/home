# scripts

## Purpose

运维与数据类脚本：数据库初始化、数据导入/备份等，在项目根目录或指定环境下执行。

## Structure

| 文件 | 说明 |
|------|------|
| init_db.py | 数据库初始化（依赖 core.config、mysqlengine.Base 等） |
| import_mongodb_data.py | 从 MongoDB 导入数据 |
| save_dbback.py | 数据库备份 |
| data/ | 数据相关文件或脚本 |

## Key Conventions

- 脚本通常需在正确配置环境变量后执行（如数据库连接来自 core.config）。
- 不通过 uvicorn 运行，独立进程执行。

## Used By

运维、部署或开发时手动/定时执行。
