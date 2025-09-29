PY=uv run
PKG=f1api

.PHONY: setup lint fmt type test migrate seed run up down build check

setup:
	uv venv
	uv sync
	pre-commit install

lint:
	$(PY) ruff check .

fmt:
	$(PY) ruff check . --fix
	$(PY) black .

type:
	$(PY) mypy $(PKG)

test:
	PYTHONPATH=. $(PY) pytest -q

MIGRATE?=head
migrate:
	$(PY) alembic upgrade $(MIGRATE)

seed:
	PYTHONPATH=. $(PY) python -m f1api.services.seed_2024

run:
	$(PY) uvicorn $(PKG).main:app --host 0.0.0.0 --port 8000 --reload

up:
	docker compose up --build

down:
	docker compose down -v

build:
	docker build -t f1api:local .

check: lint type test
