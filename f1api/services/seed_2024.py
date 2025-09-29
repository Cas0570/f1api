from __future__ import annotations

from datetime import date, datetime
from typing import Any, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from f1api.core.db import SessionLocal
from f1api.models import (
    Base,
    Circuit,
    Driver,
    Entry,
    Event,
    Season,
    SessionResult,
    SessionType,
    Team,
)
from f1api.models import (
    Session as RaceSession,
)

T = TypeVar("T", bound=Base)


def get_or_create(
    session: Session, model: type[T], defaults: dict[str, Any] | None = None, **kwargs: Any
) -> tuple[T, bool]:
    stmt = select(model).filter_by(**kwargs)
    obj = session.execute(stmt).scalar_one_or_none()
    if obj:
        return obj, False
    params = {**kwargs, **(defaults or {})}
    obj = model(**params)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj, True


def seed_minimal_2024() -> None:
    """Idempotent minimal seed: season 2024, Bahrain GP, RBR entries, race results 1-2."""
    db = SessionLocal()
    try:
        season, _ = get_or_create(db, Season, year=2024)

        rbr, _ = get_or_create(
            db, Team, ref="red_bull_racing", defaults={"name": "Red Bull Racing"}
        )

        max_drv, _ = get_or_create(
            db,
            Driver,
            ref="max_verstappen",
            defaults={
                "code": "VER",
                "permanent_number": 1,
                "first_name": "Max",
                "last_name": "Verstappen",
                "date_of_birth": date(1997, 9, 30),
                "nationality": "Dutch",
                "country_code": "NLD",
            },
        )

        checo_drv, _ = get_or_create(
            db,
            Driver,
            ref="sergio_perez",
            defaults={
                "code": "PER",
                "permanent_number": 11,
                "first_name": "Sergio",
                "last_name": "Pérez",
                "date_of_birth": date(1990, 1, 26),
                "nationality": "Mexican",
                "country_code": "MEX",
            },
        )

        e_max, _ = get_or_create(
            db,
            Entry,
            season_id=season.id,
            driver_id=max_drv.id,
            team_id=rbr.id,
            defaults={"car_number": 1},
        )
        e_checo, _ = get_or_create(
            db,
            Entry,
            season_id=season.id,
            driver_id=checo_drv.id,
            team_id=rbr.id,
            defaults={"car_number": 11},
        )

        sakhir, _ = get_or_create(
            db,
            Circuit,
            ref="sakhir",
            defaults={
                "name": "Bahrain International Circuit",
                "country_code": "BHR",
                "city": "Sakhir",
            },
        )

        bah_gp, _ = get_or_create(
            db,
            Event,
            season_id=season.id,
            circuit_id=sakhir.id,
            round=1,
            defaults={"name": "Bahrain Grand Prix"},
        )

        # Create three sessions (FP, Q, Race) with a simple order
        _fp, _ = get_or_create(
            db,
            RaceSession,
            event_id=bah_gp.id,
            type=SessionType.FP,
            session_order=1,
            defaults={"name": "Practice", "started_at": datetime(2024, 2, 29, 12, 0, 0)},
        )
        _q, _ = get_or_create(
            db,
            RaceSession,
            event_id=bah_gp.id,
            type=SessionType.QUALIFYING,
            session_order=2,
            defaults={"name": "Qualifying", "started_at": datetime(2024, 3, 1, 18, 0, 0)},
        )
        race, _ = get_or_create(
            db,
            RaceSession,
            event_id=bah_gp.id,
            type=SessionType.RACE,
            session_order=3,
            defaults={"name": "Race", "started_at": datetime(2024, 3, 2, 18, 0, 0)},
        )

        # Race results 1-2 for RBR
        get_or_create(
            db,
            SessionResult,
            session_id=race.id,
            entry_id=e_max.id,
            defaults={"position": 1, "points": 25.0, "status": "FINISHED", "laps": 57, "grid": 1},
        )
        get_or_create(
            db,
            SessionResult,
            session_id=race.id,
            entry_id=e_checo.id,
            defaults={"position": 2, "points": 18.0, "status": "FINISHED", "laps": 57, "grid": 5},
        )

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_minimal_2024()
