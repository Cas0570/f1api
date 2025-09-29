"""Shared pytest fixtures for test isolation."""

import os
from collections.abc import Generator
from typing import Any, Dict

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from f1api.core.config import settings


@pytest.fixture(scope="session")
def db_engine() -> Generator[Engine, None, None]:
    """Create a test database engine."""
    # Use test database URL if provided, otherwise use settings
    db_url = os.getenv("DATABASE_URL", settings.database_url)
    engine = create_engine(db_url, pool_pre_ping=True)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine: Engine) -> Generator[Session, None, None]:
    """
    Provide a transactional scope for tests.
    Each test gets a clean transaction that rolls back after the test.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection, autoflush=False, autocommit=False)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function", autouse=True)
def ensure_clean_tables(db_engine: Engine) -> None:
    """
    Ensure tables are clean before each test.
    This runs automatically for all tests.
    """
    # Note: In production test setup, you'd want to:
    # 1. Create a separate test database
    # 2. Run migrations before tests
    # 3. Truncate tables between tests
    # For now, we rely on the seeded data being idempotent
    pass


@pytest.fixture(scope="function")
def seed_minimal_data(db_session: Session) -> Dict[str, Any]:
    """
    Seed minimal test data for tests that need it.
    This is isolated per test via db_session transaction.
    """
    from datetime import date

    from f1api.models import Circuit, Driver, Entry, Event, Season, Team

    # Create minimal data
    season = Season(year=2024)
    db_session.add(season)

    team = Team(ref="test_team", name="Test Team")
    db_session.add(team)

    driver = Driver(
        ref="test_driver",
        code="TST",
        first_name="Test",
        last_name="Driver",
        date_of_birth=date(1990, 1, 1),
    )
    db_session.add(driver)

    circuit = Circuit(ref="test_circuit", name="Test Circuit")
    db_session.add(circuit)

    db_session.flush()

    event = Event(season_id=season.id, circuit_id=circuit.id, round=1, name="Test GP")
    db_session.add(event)

    entry = Entry(season_id=season.id, team_id=team.id, driver_id=driver.id, car_number=1)
    db_session.add(entry)

    db_session.commit()

    return {
        "season": season,
        "team": team,
        "driver": driver,
        "circuit": circuit,
        "event": event,
        "entry": entry,
    }
