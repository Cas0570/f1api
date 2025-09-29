# F1 API Agent Guide

## Scope

-   These instructions cover the entire repository.

## Quick project orientation

-   FastAPI app entrypoint lives in `f1api/main.py`; keep the `/healthz`, `/metrics`, and `_debug/boom` endpoints intact unless the product requirements change.
-   All public routes must hang off the `/api/v1` router—add new routers/modules to `f1api/api/` and register them in `f1api/api/router.py`.

## Workflow expectations

1. **Environment setup:** run `make setup` once per clone to create the uv-managed venv and install hooks.
2. **Before committing:** run `make check` (ruff lint + mypy + pytest). Use `make fmt` for auto-fixes. Invoke extra targets (`make migrate`, `make seed`, `make run`, `make up`/`make down`) as needed.
3. **Database changes:** every schema/model change requires an Alembic migration plus updates to the seed script or fixtures.
4. **PR / handoff message:** include a short summary plus every command you ran (and its status) so reviewers can reproduce quickly.

## Code & style conventions

-   Target Python 3.13 and keep everything fully typed (`disallow_untyped_defs = true`). Prefer modern SQLAlchemy 2.x patterns with the shared sync session (`SessionLocal`/`get_db`).
-   Formatters: Black + Ruff with 100-character lines. Let Ruff handle import sorting; don’t fight the hooks.
-   Raise typed HTTP exceptions with structured JSON payloads that match the global handlers.

## API and schema guidance

-   New endpoints should follow the existing sync FastAPI pattern: router in `f1api/api/<feature>.py`, dependency-injected DB session, and Pydantic read models declared in `f1api/schemas/` (remember to export them in `f1api/schemas/__init__.py`).
-   Maintain pagination/query conventions (`limit`, `offset`, simple equality filters) and reuse `Query` parameter validation.
-   When touching error or response shapes, verify they still conform to the shared exception handlers.

## Data layer & migrations

-   Use `f1api.core.db.get_db` for request-scoped sessions; never create ad-hoc engines.
-   Any new tables/columns: add SQLAlchemy models, write an Alembic migration, and extend the minimal 2024 seed data to keep API tests passing. The seed script must stay idempotent.

## Tests

-   Add or extend pytest modules under `tests/`. Use `httpx.AsyncClient` with `ASGITransport` to exercise FastAPI routes and cover both success and failure cases.
-   Keep regression coverage for seeds, migrations, and the debug endpoint when relevant.

## Configuration & docs

-   Respect `f1api.core.config.Settings`; new settings need sensible defaults and `.env` overrides.
-   Update the README when you add commands, endpoints, or workflows so `make` targets stay discoverable.
