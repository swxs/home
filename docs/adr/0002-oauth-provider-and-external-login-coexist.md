# OAuth Provider 与 External OAuth Login 并存

同一 system 模块同时承担两种 OAuth 角色：作为 **OAuth Provider** 向第三方 client 签发 code/token（`/api/oauth/*`），以及作为 **External OAuth Login** 消费 GitHub 等外部提供商、写入 GITHUB 类型 Auth Method（`/api/system/auth/github_*`）。

两者共享 User / Auth Method 身份模型但协议路径完全分离，避免把「平台授权第三方」与「用户用 GitHub 登录本平台」混在同一套端点里。代价是讨论 OAuth 时必须带前缀（Provider vs External Login），否则语义歧义。
