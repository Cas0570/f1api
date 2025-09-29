# F1 API (FastAPI + SQLAlchemy + Alembic)

MVP JSON API for Formula 1 data. Tooling uses **uv** for packaging & venvs, with Black, Ruff, MyPy, pytest, Docker, and docker-compose.

## Quickstart

```bash
# 1) Setup env & deps
uv venv
uv sync
pre-commit install

# 2) Run app
make run
# open http://localhost:8000/healthz

# 3) Tests
make test

# 4) Docker (API + Postgres)
cp .env.example .env
make up
```
