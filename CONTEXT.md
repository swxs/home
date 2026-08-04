# Home 后端

面向个人与家庭场景的 FastAPI 业务平台；以 User 为身份根，各子应用通过 user_id 挂载。无多租户或组织模型。

## Language

### 身份与认证

**User**:
平台用户档案，含显示名、头像等；本身不表达「能否登录」。口语「账号」若指档案本身，即 User。
_Avoid_: account, 用户表, 账号（指登录凭据或验证状态时）

**Auth Method**:
User 的一种登录或外部绑定方式，由类型、标识、凭证、验证状态组成（代码实体 `UserAuth`）。
_Avoid_: 认证记录, 登录方式（泛称）

**Verification**:
某 Auth Method 是否已完成确认（如邮箱已验证、微信已绑定）；取值 VERIFIED / UNVERIFIED。
_Avoid_: 激活, 激活状态, active（与 OAuth Client 启用状态混淆时）

**Identity**:
User 与其 Auth Methods 的聚合，用于解析「这个人是谁、通过什么方式认出来」；不是单独持久化的实体。
_Avoid_: 身份表, 账户

**Login Password**:
PASSWORD 类型 Auth Method 的凭证，bcrypt 哈希存储。
_Avoid_: password（无前缀）, 密码（在密码库语境下）

**Registration**:
创建 User 并同时建立 PASSWORD 与 EMAIL 两条 Auth Method；两者均 VERIFIED 后才允许登录。
_Avoid_: signin, 旧版登录

**Legacy Sign-in**:
遗留 signin 端点：创建 User 与单条 Auth Method，无邮箱验证要求；新用户应走 Registration。
_Avoid_: register, 注册

### OAuth

**OAuth Provider**:
本平台作为授权方，向第三方 OAuth Client 签发 authorization code 与 access token（路由 `/api/oauth/*`）。
_Avoid_: OAuth, 授权服务器（无前缀）

**OAuth Client**:
在本平台注册的第三方应用；is_active 表示客户端是否可用，与用户 Verification 无关。
_Avoid_: 客户端（HTTP client 语境）, app

**Authorization Grant**:
User 已对某 OAuth Client 完成授权的记录（代码实体 `OAuthUserGrant`）。
_Avoid_: grant, 授权（泛称）

**External OAuth Login**:
通过外部身份提供商（如 GitHub）登录，在本平台写入对应 Auth Method；不走 OAuth Provider 流程。
_Avoid_: OAuth 登录（无前缀）

### 密码库

**Vault Entry**:
用户个人密码库中的一条记录，含标识（key）、名称、关联网站（代码实体 `PasswordLock`）。
_Avoid_: 密码锁, password lock, 密码（指登录密码时）

**Vault Secret**:
Vault Entry 所保护的实际密码值；COMMON 类型从加密库按 key 解密，CUSTOM 类型存于条目 JSON。
_Avoid_: password, credential

**Reveal**:
解密并返回 Vault Secret 的操作；会递增条目的 used 计数。
_Avoid_: 查看密码, decrypt

### 文件与分享

**Stored File**:
已上传至对象存储的文件的元数据；file_id 为内容 MD5，也是存储键依据（代码实体 `FileInfo`）。
_Avoid_: 文件, upload file

**Share Link**:
通过 token 公开访问 Stored File 的链接，有 ACTIVE / REVOKED 状态与过期时间（代码实体 `FileShareLink`）。
_Avoid_: 分享 URL（指完整 URL 字符串时）

### 数独

**Puzzle**:
一道 81 格数独题目，含 puzzle_date（每日一题）与难度（代码实体 `SudokuPuzzle`）。
_Avoid_: 谜题, sudoku

**Completion**:
某 User 完成某 Puzzle 的记录；同一 User + Puzzle 唯一（代码实体 `SudokuCompletion`）。
_Avoid_: 完成记录, solve record

### 微信

**WeChat Binding**:
WECHAT 类型 Auth Method，标识为 openid；关注公众号时建立或恢复，取关时 Verification 降为 UNVERIFIED（解绑语义）。
_Avoid_: 微信用户, wechat account

### 通知

**Notification Channel**:
notify 模块下的投递渠道（当前仅有 email）；负责发送与记录，不修改身份状态。
_Avoid_: notify, 通知服务

**Outbound Email**:
通过 SMTP 发出的邮件，含验证、重置密码等模板；每次发送产生一条发送记录。
_Avoid_: 邮件, email message

**Delivery Token**:
存于 Redis、带 TTL 的一次性令牌，用于邮箱验证或密码重置链接。
_Avoid_: token, verify token, reset token（无前缀时）

## Relationships

- 一个 **User** 拥有多条 **Auth Method**；`(ttype, identifier)` 全局唯一。
- **Registration** 为每个新 User 创建 PASSWORD 与 EMAIL 两条 Auth Method；验证后两者同时变为 VERIFIED。
- **Vault Entry**、**Completion**、**Authorization Grant** 均归属一个 **User**。
- 一个 **Stored File** 可有多条 **Share Link**；token 唯一。
- 一个 **Puzzle** 可被多个 User 各自产生 **Completion**；同一 User + Puzzle 仅一条。
- **Outbound Email** 由 **Notification Channel** 投递；身份变更仍由 system 认证模块负责。
