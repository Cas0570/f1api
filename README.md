# 🏎️ F1 API

[![CI](https://github.com/Cas0570/f1api/actions/workflows/ci.yml/badge.svg)](https://github.com/Cas0570/f1api/actions/workflows/ci.yml)

A Formula 1 data API built with **FastAPI**, **SQLAlchemy**, **Alembic**, and **Postgres**.
It exposes seasons, drivers, teams, circuits, events, sessions, and results — starting with **comprehensive 2024 season data** (10 teams, 20 drivers, 6 races).

---

## 🚀 Features (MVP)

-   `/healthz` endpoint for liveness checks
-   `/metrics` stub endpoint (Prometheus-compatible placeholder)
-   CRUD-ready DB layer with SQLAlchemy 2.0
-   Alembic migrations for schema evolution
-   Comprehensive 2024 season seed data:
    -   **10 teams** (Red Bull, Ferrari, Mercedes, McLaren, Aston Martin, Alpine, Williams, RB, Kick Sauber, Haas)
    -   **20 drivers** (full 2024 grid)
    -   **6 circuits** (Bahrain, Saudi Arabia, Australia, Japan, China, Miami)
    -   **6 races** with realistic results and standings
-   Read-only API for:
    -   **Seasons** (`/api/v1/seasons`)
    -   **Drivers** (`/api/v1/drivers`)
    -   **Teams** (`/api/v1/teams`)
    -   **Events** (`/api/v1/events`)
    -   **Standings** (`/api/v1/standings/drivers`, `/api/v1/standings/constructors`)
-   **Paginated responses** with metadata (total, limit, offset, page, pages)
-   Filters & pagination (e.g. `/api/v1/events?season_year=2024`)
-   Full test suite (`pytest + httpx`)
-   Pre-commit hooks (Ruff, Black, MyPy)
-   **Automated CI/CD** with GitHub Actions ⭐ NEW
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
-   Seed comprehensive 2024 dataset (10 teams, 20 drivers, 6 races)
-   Start the API on port 8000

### 2. Stop services

```bash
make down
```

---

## 🔄 Continuous Integration

Every push and pull request automatically runs:

-   **Linting** (Ruff) - Code style checks
-   **Type checking** (MyPy) - Static type verification
-   **Tests** (pytest) - Full test suite with real database
-   **Docker build** - Ensures image builds successfully

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for details.

---

## 🔎 Quick API Tests

### Health check

```bash
curl http://localhost:8000/healthz
```

### List all 20 drivers

```bash
curl http://localhost:8000/api/v1/drivers | jq '.items[] | {name: (.first_name + " " + .last_name), code: .code}'
```

### Filter driver by code

```bash
curl "http://localhost:8000/api/v1/drivers?code=VER" | jq
```

### List all 10 teams

```bash
curl http://localhost:8000/api/v1/teams | jq '.items[] | {name: .name}'
```

### List all 6 races

```bash
curl "http://localhost:8000/api/v1/events?season_year=2024" | jq '.items[] | {round: .round, name: .name}'
```

### Get driver standings after 6 races

```bash
curl "http://localhost:8000/api/v1/standings/drivers?season_year=2024&limit=10" | jq '.items[] | {pos: .position, driver: (.driver_first_name + " " + .driver_last_name), points: .points, wins: .wins}'
```

Expected top 5:

1. Max Verstappen - 118 pts, 4 wins
2. Sergio Pérez - 91 pts, 0 wins
3. Charles Leclerc - 84 pts, 0 wins
4. Lando Norris - 78 pts, 1 win
5. Carlos Sainz - 75 pts, 1 win

### Get constructor standings

```bash
curl "http://localhost:8000/api/v1/standings/constructors?season_year=2024" | jq '.items[] | {pos: .position, team: .team_name, points: .points, wins: .wins}'
```

Expected top 3:

1. Red Bull Racing - 209 pts, 4 wins
2. Ferrari - 159 pts, 1 win
3. McLaren - 116 pts, 1 win

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

-   Expand to full 24-race 2024 calendar
-   Add qualifying session results
-   Replace `/metrics` stub with real Prometheus exporter
-   Add structured logging
-   Add API key authentication
-   Add caching layer (Redis)

---
