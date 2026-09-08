# syntax=docker/dockerfile:1

# ── Stage 1: 构建依赖 ──
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
RUN uv sync --frozen --no-dev --no-editable

# ── Stage 2: 运行时 ──
FROM python:3.13-slim-bookworm AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    TZ=Asia/Shanghai

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY assets ./assets
COPY logging.ini ./logging.ini

RUN useradd --create-home appuser \
    && mkdir -p /app/logs /app/temp \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "home.main:app", "--host", "0.0.0.0", "--port", "8000"]
