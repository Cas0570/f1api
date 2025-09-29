FROM python:3.13-slim

# System deps
RUN apt-get update && apt-get install -y \
    curl build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install uv and ensure it's in PATH
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
 && mv /root/.local/bin/uv /usr/local/bin/uv \
 && mv /root/.local/bin/uvx /usr/local/bin/uvx

WORKDIR /app

# Copy pyproject + lock first (layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy app
COPY . .

# Default command
CMD ["uv", "run", "uvicorn", "f1api.main:app", "--host", "0.0.0.0", "--port", "8000"]
