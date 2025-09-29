FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    UV_SYSTEM_PYTHON=1 \
    PATH="/root/.local/bin:${PATH}"

# system deps (curl required to install uv)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

# copy project files for dependency resolution
COPY pyproject.toml uv.lock ./
# sync dependencies (prod only inside image)
RUN uv sync --frozen --no-dev

# now copy source
COPY f1api ./f1api

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "f1api.main:app", "--host", "0.0.0.0", "--port", "8000"]
