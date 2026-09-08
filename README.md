# home

## 环境搭建

```
uv sync
```

## 构建镜像

sh ./get_base.sh

## 启动项目

```
uv run uvicorn home.main:app --reload --port 8090
```

## 主要功能

- 用户注册
- 密码管理
- 临时文档
- GitHub OAuth登录

## 项目结构

整体架构与各目录职责见 [CONTEXT.md](./CONTEXT.md) 与 [docs/architecture/project-overview.md](./docs/architecture/project-overview.md)。主应用代码位于 `src/home/`，爬虫位于 `spiders/`，静态资源位于 `assets/`。

## GitHub OAuth 配置

如需使用GitHub OAuth登录功能，请参考 [GitHub OAuth配置指南](./docs/GITHUB_OAUTH_SETUP.md) 获取Client ID和Client Secret。

## OSS 文件直传

`openapi_file` 使用 `/api/upload/presign/*` 获取阿里云 OSS 临时上传/下载地址。可配置：

```env
UPLOAD_MAX_BYTES=524288000
UPLOAD_PRESIGN_EXPIRES=600
DOWNLOAD_PRESIGN_EXPIRES=600
CORS_ALLOWED_ORIGINS=http://127.0.0.1:8084,http://localhost:8084
```

OSS Bucket 需允许 openapi_file 的实际域名执行 `PUT`、`GET`、`HEAD`，允许
`Content-Type`、`Content-MD5`、`Range` 请求头，并暴露 `ETag`、
`Content-Length`、`Content-Range`、`x-oss-request-id`。

历史 `file_info` 和 MD5-only OSS key 必须在部署新版本前迁移：

```powershell
uv run python scripts/migrate_file_info_storage.py --user-id <USER_OBJECT_ID> --dry-run
uv run python scripts/migrate_file_info_storage.py --user-id <USER_OBJECT_ID>
```

脚本会把对象重刷为 `{md5前4位}/{md5剩余}-{file_size}`，回填指定用户，并在新对象和数据库均确认成功后删除旧 key。
