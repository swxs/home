# PowerShell 版本的构建脚本
$ErrorActionPreference = "Stop"

# 计算 pyproject.toml 的 MD5 哈希值（前16位）作为版本标签
$hash = (Get-FileHash -Path ./pyproject.toml -Algorithm MD5).Hash.Substring(0, 16)

Write-Host "构建镜像: swxs/home:$hash"
docker build -t swxs/home:$hash .

if ($LASTEXITCODE -ne 0) {
    Write-Error "构建镜像失败"
    exit 1
}

Write-Host "推送镜像: swxs/home:$hash"
docker push swxs/home:$hash

if ($LASTEXITCODE -ne 0) {
    Write-Error "推送镜像失败"
    exit 1
}

Write-Host "标记为 latest 并推送"
docker image tag swxs/home:$hash swxs/home:latest
docker push swxs/home:latest

if ($LASTEXITCODE -ne 0) {
    Write-Error "推送 latest 标签失败"
    exit 1
}

Write-Host "构建完成！"

