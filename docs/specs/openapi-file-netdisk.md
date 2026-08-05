# Spec: openapi_file — Personal Netdisk with Presigned OSS Upload

**Status:** ready-for-agent  
**Repos:** `home` (backend `apps/upload`), `openapi_file` (new Vue frontend)  
**Labels:** `ready-for-agent`

---

## Problem Statement

用户需要一个最简单的个人网盘能力：上传文件、查看「我的文件」、删除、创建分享链接、在线预览。当前 `home/apps/upload` 已有 `FileInfo`（Stored File）、`FileShareLink`（Share Link）与阿里云 OSS 集成，但存在以下缺口：

- **无用户隔离**：`FileInfo` 无 `user_id`，列表 API 返回全局文件，无法支撑「我的网盘」
- **服务端中转上传**：`POST /api/upload/upload/` 将文件全量经 API 服务器写入 OSS，不适合大文件与高并发
- **无 Presigned 直传**：缺少业界标准的「申请 URL → 客户端直传 OSS → 确认落库」流程
- **无前端**：`openapi_auth` / `openapi_user` 系列尚无文件管理 UI

Share Link 模块已按 `create_by` 做用户隔离，可复用；FileInfo 与上传链路需扩展。

## Solution

新建 `openapi_file` Vue 3 前端（对齐 `openapi_user` 技术栈与 OAuth2 流程），对接扩展后的 `home/apps/upload` API。后端引入 Presigned 直传阿里云 OSS：客户端先计算 MD5，申请上传 URL，直传 OSS 后调用 `/complete` 校验并写入完整 `FileInfo`（含 `user_id`）。相同 MD5 内容全局共享 OSS 对象（秒传），元数据按用户隔离。前端以虚拟文件夹（按扩展名/日期分组）展示扁平列表，内联分享操作，支持图片/视频/PDF 富预览。

## Reference Projects

| 类型 | 项目 | 借鉴点 |
|------|------|--------|
| API 层 | [lyushher/file-upload-service](https://github.com/lyushher/file-upload-service) | FastAPI + Presigned URL + DB 元数据 |
| API 层 | [upload-infra](https://github.com/SSarkar0307/npm-package-upload-infra) | `/upload-url` + `/complete` + HeadObject 校验 |
| API 层 | [Copubah/s3-presigned-url-api](https://github.com/Copubah/s3-presigned-url-api) | 上传/下载 Presigned 端点设计 |
| 控制台 UX | [Stowage](https://github.com/stowage-dev/stowage) | 对象浏览器、预览 drawer、内联分享 |
| 控制台 UX | [Buktio](https://github.com/buktio/buktio) | 自托管文件管理面板 |
| 云厂商 | [阿里云 OSS Presigned URL](https://www.alibabacloud.com/help/en/oss/user-guide/upload-files-using-presigned-urls) | PUT 直传签名规范 |

## User Stories

1. As an OAuth-authenticated user, I want to log in via the same authorization code flow as `openapi_user`, so that I have a consistent experience across openapi apps.
2. As a user, I want to upload files by selecting them in the browser, so that they appear in my file list without routing bytes through the API server.
3. As a user uploading a file that already exists in OSS (same MD5), I want instant upload (秒传) without re-transferring bytes, so that duplicates save time and bandwidth.
4. As a user, I want to see only my files in the file list, so that my netdisk is private to me.
5. As a user, I want files grouped visually by extension or date (virtual folders), so that I can browse a flat backend without real directory trees.
6. As a user, I want to delete a file from my netdisk, so that it disappears from my list (OSS object removed only when no other user references the same content).
7. As a user, I want to create a share link from a file row, so that I can share files with others without giving them my account access.
8. As a user, I want to view and revoke my share links in the same UI (inline/tab), so that I manage shares alongside files.
9. As a user, I want to preview images, videos, and PDFs in the browser, so that I do not need to download every file to view it.
10. As a recipient, I want to access a shared file via `/api/upload/share/{token}` without logging in, so that share links work for external users.
11. As a user, I want upload progress feedback during direct OSS transfer, so that I know large uploads are proceeding.
12. As an operator, I want existing Aliyun OSS configuration (`oss2_helper`) reused, so that deployment stays consistent with current `home` setup.

## Implementation Decisions

### Domain model

- **File Content**（OSS 层）：以 `(file_id, file_size)` 作为内容身份，其中 `file_id` 为内容 MD5，`file_size` 作为第二判据降低哈希碰撞风险；相同组合只存一份。
- **Stored File**（`FileInfo`）：某 User 对某 File Content 的元数据记录，含 `user_id`、`file_name`、`file_size`、`ext`、`policy`；同一 User + 同一 `(file_id, file_size)` 唯一。
- **Instant Upload**：申请 Presigned 时 OSS 已存在该 key → 跳过 PUT，仅创建用户 `FileInfo`。
- **Virtual Folder**：纯前端展示概念，按扩展名或上传日期分组；后端无 `parent_id` / folder 实体。

### Database changes (`FileInfo`)

- 新增 `user_id`（`ObjectIdType`，最终为非空，索引 `idx_file_info_user_id`）。
- 新增唯一约束 `(user_id, file_id, file_size)`，防止同一用户重复添加相同内容。
- 新上传对象使用同时编码 MD5 与大小的 object key（`{md5[:4]}/{md5[4:]}-{file_size}`），避免相同 MD5、不同大小的文件覆盖同一 OSS 对象。
- 删除文件时：删除该用户的 `FileInfo` 行；若全局无其他 `FileInfo` 引用该 `(file_id, file_size)`，再删除 OSS 对象（引用计数逻辑在 service 层）。
- 历史数据通过迁移脚本统一重刷：命令必须指定目标 `user_id`，将旧 object key（`{md5[:4]}/{md5[4:]}`）搬迁为新 key，回填 `user_id`，保持原 FileInfo ID 与 Share Link 引用。运行时代码不保留旧 key 兼容逻辑。

### Historical data migration

- 提供可重复执行的迁移脚本，参数至少包含 `--user-id <target_user_id>` 与 `--dry-run`。
- 迁移顺序：添加 nullable `user_id` → 校验旧 OSS 对象及 `file_size` → 复制到新 key → HeadObject 校验新对象 → 回填指定 `user_id` → 删除旧 key。
- 数据库回填成功前不得删除旧 key；目标 key 已存在且大小一致时按成功处理，保证脚本可幂等重跑。
- 旧对象缺失、目标大小冲突或数据库回填失败时记录错误并保留旧对象，不得静默覆盖或删除。
- 全部历史行迁移成功后，将 `user_id` 改为非空并建立 `(user_id, file_id, file_size)` 唯一约束。

### Presigned upload flow

```text
1. Client: Web Worker 分块计算 MD5 → file_id
2. POST /api/upload/presign/upload
   Body: { file_id, file_name, file_size, content_type }
   Auth: Bearer token (OAuth access_token)
3. Server:
   a. HeadObject(file_id key) — exists?
   b. If exists AND user has no FileInfo for this (file_id, file_size):
      → create FileInfo, return { skip_upload: true, data: FileInfoOut }
   c. If exists AND user already has FileInfo for this (file_id, file_size):
      → return existing FileInfo with HTTP 200 (idempotent)
   d. If not exists:
      → sign PUT URL (Content-Type must match client upload)
      → do not create a PENDING record; defer FileInfo creation until /complete
      → return { skip_upload: false, presigned_url, expires_in, file_id }
4. Client: PUT presigned_url with file bytes + Content-Type header
5. POST /api/upload/presign/complete
   Body: { file_id, file_name, file_size, content_type }
6. Server:
   a. HeadObject — verify size, content-type
   b. Create or finalize FileInfo with user_id
   c. Return FileInfoOut
```

### OSS helper extensions (`commons/Helpers/ApiHelper_oss2.py`)

- `sign_put_url(path, content_type, expires)` — Presigned PUT for upload.
- `sign_get_url(path, content_disposition, expires)` — Presigned GET for preview/download (extend existing `get_sign_download_path`).
- Reuse existing `head_object` / `exists` / `delete` for complete flow and refcount cleanup.

### API contracts (new / modified)

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/api/upload/presign/upload` | token | 申请 Presigned PUT 或秒传 |
| POST | `/api/upload/presign/complete` | token | 校验 OSS 并写入 FileInfo |
| GET | `/api/upload/presign/download/{file_info_id}` | token | 返回 Presigned GET URL（预览/下载） |
| GET | `/api/upload/file_info/` | token | **Modified:** 仅返回当前 `user_id` 的文件 |
| DELETE | `/api/upload/file_info/{id}` | token | **Modified:** 删除用户记录 + 条件删 OSS |
| POST | `/api/upload/upload/` | token | **Deprecated:** 保留服务端中转兼容，按当前 User 写入 FileInfo |
| GET/POST/PUT/DELETE | `/api/upload/share_link/*` | token | 不变，已按 `create_by` 隔离 |
| GET | `/api/upload/share/{token}` | — | 不变，公开访问 |

Request/response envelope: 现有 `SuccessResponse` / exception types。

**Presign upload response (example):**

```json
{
  "skip_upload": false,
  "presigned_url": "https://...",
  "expires_in": 600,
  "file_id": "abc123...",
  "data": null
}
```

**Complete request:** `{ "file_id", "file_name", "file_size", "content_type" }`

### Authorization

- 所有 `file_info` 与 `presign` 端点要求 `get_token`（与现有 `file_share_link` 一致）。
- 用户只能 list/get/delete 自己的 `FileInfo`（`user_id == token.user_id`）。
- 旧版 `POST /api/upload/upload/` 不在新前端使用；为满足 `user_id` 非空和隔离要求，端点改为必须携带 token，并按当前 User 写入 FileInfo。

### Frontend (`openapi_file`)

- **Scaffold:** 复制 `openapi_user` 项目结构（Vue 3 + Vue Router 4 + ant-design-vue 4 + axios + less）。
- **Auth:** 复用 `src/utils/oauth.js`、`src/utils/auth.js`、`src/plugins/axios.js` 模式；独立 OAuth Client 注册（新 `client_id` / redirect URI）。
- **Env:**

  ```env
  VUE_APP_API_BASE_URL=http://127.0.0.1:8090
  VUE_APP_OAUTH_SERVER_URL=http://127.0.0.1:8090
  VUE_APP_OAUTH_CLIENT_ID=<file-app-client-id>
  VUE_APP_OAUTH_REDIRECT_URI=http://127.0.0.1:<port>/oauth/callback
  VUE_APP_OAUTH_SCOPE=read write
  ```

- **Pages / routes:**
  - `/` — 文件列表（虚拟文件夹 Tab：全部 / 图片 / 文档 / 其他；或按日期分组）
  - `/oauth/callback` — OAuth 回调
  - 分享管理：文件列表页内 Tab「我的分享」
  - 公开分享页 **不在** openapi_file 内实现（仍由 `GET /api/upload/share/{token}` 直接响应或由 future 静态页处理）

- **Upload UX:**
  - ant-design-vue `Upload` 或自定义 dropzone
  - 选择文件 → Web Worker MD5（推荐 `spark-md5`）→ presign → XHR/fetch PUT to OSS with progress → complete → refresh list

- **Preview:**
  - 图片：`presign/download` URL → `<img>` / lightbox
  - 视频：`<video src="presigned_url">`
  - PDF：`<iframe>` or pdf.js with presigned URL
  - 其他：触发下载

- **Share inline:** 文件行操作「分享」→ modal 创建 Share Link → 复制 URL；Tab 列出 share_link API 结果，支持 revoke/delete。

### Content-Type enforcement

- Presigned PUT 生成时绑定 `Content-Type`；客户端 PUT 必须携带相同 header，否则 OSS 403。
- 可选白名单：扩展 `consts` 允许 MIME 列表（参考 Copubah/s3-presigned-url-api）。

### File size limits

- 配置项：`UPLOAD_MAX_BYTES`（env），presign 阶段校验 `file_size`。
- 超大文件（>5GB）multipart presigned 作为 **out of scope**；文档注明单 PUT 上限。

## Testing Decisions

### Primary test seam: `UploadService` / new `PresignUploadService`

Injectable: `FileInfoRepository`, `oss2_helper` (mock HeadObject, sign_url, delete).

| Scenario | Expected |
|----------|----------|
| Presign, OSS missing | Returns presigned_url, skip_upload=false |
| Presign, OSS exists, user has no record | Creates FileInfo, skip_upload=true |
| Presign, OSS exists, user already has record | Returns existing with HTTP 200 |
| Complete, OSS object matches size/type | FileInfo created with user_id |
| Complete, OSS object missing | 400 error |
| Complete, size mismatch | 400 error |
| Delete file, last user reference | FileInfo deleted + OSS object deleted |
| Delete file, other user references same `(file_id, file_size)` | FileInfo deleted, OSS retained |
| List file_info | Only current user's records |

### Secondary seam: `FileShareLinkService`

Existing tests if any; ensure create still works with user-scoped FileInfo ownership check (user can only share own files).

### Prior art

- `tests/apps/repository_migration_tests.py` — async service tests
- `apps/upload/services/upload_service.py` — existing OSS + repo patterns

## Out of Scope

- 真实目录树 / Folder 实体
- 多 OSS provider（仅 Aliyun，policy=ALIOSS）
- 服务端中转上传重构（旧端点保留 deprecated）
- Multipart presigned upload（>5GB 文件）
- openapi_file 内嵌公开分享落地页（token 访问仍走 API）
- 管理端全局文件审计 UI
- 从 `openapi_user` 内嵌文件组件（独立 app）
- Celery / 异步病毒扫描
- 文件版本历史

## Further Notes

- 领域术语（**File Content**、**Stored File**、**Instant Upload**）见本文 Implementation Decisions > Domain model；若需独立 glossary 可后续从 spec 提取至 `docs/domain/`。
- OAuth Client 需在 home OAuth Provider 注册新 client，redirect URI 指向 openapi_file dev/prod 地址。
- MD5 计算在客户端；大文件使用 Web Worker + 分块读取，避免阻塞 UI。
- 全局去重意味着 User A 与 User B 上传相同文件共享 OSS 存储；元数据（文件名等）各自独立。
- 参考 Stowage/Buktio 的 UX 模式，但不引入其 S3 控制台级别的 bucket/IAM 管理 scope。
