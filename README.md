# home

## 环境搭建

```
uv sync
```

## 构建镜像

sh ./get_base.sh

## 启动项目

```
uvicorn main:app --reload --port 8090
```

## 主要功能

- 用户注册
- 密码管理
- 临时文档
- GitHub OAuth登录

## GitHub OAuth 配置

如需使用GitHub OAuth登录功能，请参考 [GitHub OAuth配置指南](./docs/GITHUB_OAUTH_SETUP.md) 获取Client ID和Client Secret。
