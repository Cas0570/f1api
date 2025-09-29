#!/bin/bash
set -e

# Wait for DB
echo "⏳ Waiting for database..."
until pg_isready -h db -U f1 -d f1api; do
  sleep 1
done

echo "✅ Database ready!"

# Run migrations
echo "🚀 Applying migrations..."
uv run alembic upgrade head

# Seed data
echo "🌱 Seeding 2024 dataset..."
uv run python -m f1api.services.seed_2024

# Start app
echo "🔥 Starting FastAPI..."
exec uv run uvicorn f1api.main:app --host 0.0.0.0 --port 8000 --reload
