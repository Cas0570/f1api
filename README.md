# 🏎️ F1 API

A Formula 1 data API built with **FastAPI**, **SQLAlchemy**, **Alembic**, and **Postgres**.
It exposes seasons, drivers, teams, circuits, events, sessions, and results — starting with a minimal **2024 seed dataset**.

---

## 🚀 Features (MVP)

-   `/healthz` endpoint for liveness checks
-   `/metrics` stub endpoint (Prometheus-compatible placeholder)
-   CRUD-ready DB layer with SQLAlchemy 2.0
-   Alembic migrations for schema evolution
-   Seed script for minimal 2024 season data
-   Read-only API for:
    -   **Seasons** (`/api/v1/seasons`)
    -   **Drivers** (`/api/v1/drivers`)
    -   **Teams** (`/api/v1/teams`)
    -   **Events** (`/api/v1/events`)
-   Filters & pagination (e.g. `/api/v1/events?season_year=2024`)
-   Full test suite (`pytest + httpx`)
-   Pre-commit hooks (Ruff, Black, MyPy)
-   Dockerized for local dev (API + Postgres)

---

## 🛠️ Local Development

### 1. Setup environment

```bash
make setup
```

This will:

-   Create a virtualenv (`.venv`)
-   Install dependencies with [uv](https://github.com/astral-sh/uv)
-   Install pre-commit hooks

### 2. Run checks

```bash
make check   # lint + type-check + test
make fmt     # auto-fix style issues
```

### 3. Run the API

```bash
make run
```

Now visit [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🐳 Run with Docker

### 1. Start services

```bash
make up
```

This will:

-   Launch Postgres
-   Run Alembic migrations
-   Seed minimal 2024 dataset
-   Start the API on port 8000

### 2. Stop services

```bash
make down
```

---

## 🔎 Quick API Tests

### Health check

```bash
curl http://localhost:8000/healthz
```

### List drivers

```bash
curl http://localhost:8000/api/v1/drivers
```

### Filter driver by code

```bash
curl "http://localhost:8000/api/v1/drivers?code=VER"
```

### Get driver by ID

```bash
curl http://localhost:8000/api/v1/drivers/1
```

### List teams

```bash
curl http://localhost:8000/api/v1/teams
```

### List seasons

```bash
curl http://localhost:8000/api/v1/seasons
```

### List events (filter by season year)

```bash
curl "http://localhost:8000/api/v1/events?season_year=2024"
```

---

## 🧪 Tests

Run test suite (with DB checks):

```bash
make test
```

---

## 📂 Project Structure

```
f1api/
 ├── api/           # FastAPI routers
 ├── core/          # Config & DB setup
 ├── models/        # SQLAlchemy models
 ├── schemas/       # Pydantic schemas
 ├── services/      # Seeding scripts, domain logic
 ├── tests/         # Pytest tests
 └── main.py        # FastAPI entrypoint
```

---

## 🔮 Next Steps

-   Add standings endpoints (drivers & constructors)
-   Expand seed data (all 2024 races & results)
-   Replace `/metrics` stub with real Prometheus exporter
-   Add structured logging & error handling

---
