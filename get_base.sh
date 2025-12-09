#!/bin/bash
set -e  # 遇到错误立即退出

# 计算 pyproject.toml 的 MD5 哈希值（前16位）作为版本标签
hash=$(md5sum ./pyproject.toml | cut -c 1-16)

echo "构建基础镜像: swxs/home_base:$hash"
docker build -f Dockerfile.base -t swxs/home_base:$hash . 

echo "推送基础镜像: swxs/home_base:$hash"
docker push swxs/home_base:$hash

echo "标记为 latest 并推送"
docker image tag swxs/home_base:$hash swxs/home_base:latest
docker push swxs/home_base:latest

echo "构建运行镜像: swxs/home"
docker build -t swxs/home .

echo "推送运行镜像: swxs/home"
docker push swxs/home

echo "构建完成！"
