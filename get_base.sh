#!/bin/bash
set -e  # 遇到错误立即退出

# 计算 pyproject.toml 的 MD5 哈希值（前16位）作为版本标签
hash=$(md5sum ./pyproject.toml | cut -c 1-16)

echo "构建镜像: swxs/home:$hash"
docker build -t swxs/home:$hash .

echo "推送镜像: swxs/home:$hash"
docker push swxs/home:$hash

echo "标记为 latest 并推送"
docker image tag swxs/home:$hash swxs/home:latest
docker push swxs/home:latest

echo "构建完成！"
