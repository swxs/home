FROM python:3.13.11-bookworm

WORKDIR /home

# 设置时区
RUN echo 'Asia/Shanghai' > /etc/timezone \
    && ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 安装 uv
RUN python -m pip install --upgrade pip \
    && pip install uv

# 先复制依赖文件，利用Docker缓存层
COPY ./pyproject.toml ./pyproject.toml
COPY ./uv.lock ./uv.lock

# 安装依赖
RUN uv sync

# 复制所有项目文件
COPY . .

# 暴露端口
EXPOSE 8000

# 使用 uv run 运行 uvicorn
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
