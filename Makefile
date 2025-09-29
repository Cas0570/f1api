PY=uv run
PKG=f1api

.PHONY: setup lint type test migrate run up down build fmt

setup:
	uv venv
	uv sync
	pre-commit install

lint:
	uv run ruff check .

fmt:
	uv run ruff format .
	uv run black .

type:
	uv run mypy $(PKG)

test:
	PYTHONPATH=. uv run pytest -q

MIGRATE?=head
migrate:
	uv run alembic upgrade $(MIGRATE)

run:
	uv run uvicorn $(PKG).main:app --host 0.0.0.0 --port 8000 --reload

up:
	docker compose up --build

down:
	docker compose down

build:
	docker build -t f1api:local .
