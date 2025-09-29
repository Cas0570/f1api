from __future__ import annotations

from datetime import date, datetime
from typing import Any, TypedDict, TypeVar

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
from f1api.models import Session as RaceSession

T = TypeVar("T", bound=Base)


class TeamData(TypedDict):
    ref: str
    name: str


class DriverData(TypedDict):
    ref: str
    code: str
    number: int
    first: str
    last: str
    dob: date
    nat: str
    cc: str
    team: str
    car: int


class CircuitData(TypedDict):
    ref: str
    name: str
    cc: str
    city: str


class RaceResultTuple(TypedDict):
    pass  # We'll use tuples for race results


class RaceData(TypedDict):
    round: int
    circuit: str
    name: str
    date: datetime
    results: list[tuple[str, int | None, float, str, int, int]]


def get_or_create(
    session: Session, model: type[T], defaults: dict[str, Any] | None = None, **kwargs: Any
) -> tuple[T, bool]:
    """Get existing object or create new one."""
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


def seed_comprehensive_2024() -> None:  # noqa: PLR0914
    """
    Comprehensive 2024 season seed with:
    - 10 teams
    - 20 drivers
    - 6 races (Bahrain, Saudi Arabia, Australia, Japan, China, Miami)
    - Realistic race results and standings
    """
    db = SessionLocal()
    try:
        # Season
        season, _ = get_or_create(db, Season, year=2024)

        # === TEAMS ===
        teams_data: list[TeamData] = [
            {"ref": "red_bull_racing", "name": "Red Bull Racing"},
            {"ref": "ferrari", "name": "Ferrari"},
            {"ref": "mercedes", "name": "Mercedes"},
            {"ref": "mclaren", "name": "McLaren"},
            {"ref": "aston_martin", "name": "Aston Martin"},
            {"ref": "alpine", "name": "Alpine"},
            {"ref": "williams", "name": "Williams"},
            {"ref": "rb", "name": "RB"},
            {"ref": "kick_sauber", "name": "Kick Sauber"},
            {"ref": "haas", "name": "Haas F1 Team"},
        ]
        teams: dict[str, Team] = {}
        for t_data in teams_data:
            team, _ = get_or_create(db, Team, ref=t_data["ref"], defaults={"name": t_data["name"]})
            teams[t_data["ref"]] = team

        # === DRIVERS ===
        drivers_data: list[DriverData] = [
            # Red Bull Racing
            {
                "ref": "max_verstappen",
                "code": "VER",
                "number": 1,
                "first": "Max",
                "last": "Verstappen",
                "dob": date(1997, 9, 30),
                "nat": "Dutch",
                "cc": "NLD",
                "team": "red_bull_racing",
                "car": 1,
            },
            {
                "ref": "sergio_perez",
                "code": "PER",
                "number": 11,
                "first": "Sergio",
                "last": "Pérez",
                "dob": date(1990, 1, 26),
                "nat": "Mexican",
                "cc": "MEX",
                "team": "red_bull_racing",
                "car": 11,
            },
            # Ferrari
            {
                "ref": "charles_leclerc",
                "code": "LEC",
                "number": 16,
                "first": "Charles",
                "last": "Leclerc",
                "dob": date(1997, 10, 16),
                "nat": "Monégasque",
                "cc": "MCO",
                "team": "ferrari",
                "car": 16,
            },
            {
                "ref": "carlos_sainz",
                "code": "SAI",
                "number": 55,
                "first": "Carlos",
                "last": "Sainz",
                "dob": date(1994, 9, 1),
                "nat": "Spanish",
                "cc": "ESP",
                "team": "ferrari",
                "car": 55,
            },
            # Mercedes
            {
                "ref": "lewis_hamilton",
                "code": "HAM",
                "number": 44,
                "first": "Lewis",
                "last": "Hamilton",
                "dob": date(1985, 1, 7),
                "nat": "British",
                "cc": "GBR",
                "team": "mercedes",
                "car": 44,
            },
            {
                "ref": "george_russell",
                "code": "RUS",
                "number": 63,
                "first": "George",
                "last": "Russell",
                "dob": date(1998, 2, 15),
                "nat": "British",
                "cc": "GBR",
                "team": "mercedes",
                "car": 63,
            },
            # McLaren
            {
                "ref": "lando_norris",
                "code": "NOR",
                "number": 4,
                "first": "Lando",
                "last": "Norris",
                "dob": date(1999, 11, 13),
                "nat": "British",
                "cc": "GBR",
                "team": "mclaren",
                "car": 4,
            },
            {
                "ref": "oscar_piastri",
                "code": "PIA",
                "number": 81,
                "first": "Oscar",
                "last": "Piastri",
                "dob": date(2001, 4, 6),
                "nat": "Australian",
                "cc": "AUS",
                "team": "mclaren",
                "car": 81,
            },
            # Aston Martin
            {
                "ref": "fernando_alonso",
                "code": "ALO",
                "number": 14,
                "first": "Fernando",
                "last": "Alonso",
                "dob": date(1981, 7, 29),
                "nat": "Spanish",
                "cc": "ESP",
                "team": "aston_martin",
                "car": 14,
            },
            {
                "ref": "lance_stroll",
                "code": "STR",
                "number": 18,
                "first": "Lance",
                "last": "Stroll",
                "dob": date(1998, 10, 29),
                "nat": "Canadian",
                "cc": "CAN",
                "team": "aston_martin",
                "car": 18,
            },
            # Alpine
            {
                "ref": "pierre_gasly",
                "code": "GAS",
                "number": 10,
                "first": "Pierre",
                "last": "Gasly",
                "dob": date(1996, 2, 7),
                "nat": "French",
                "cc": "FRA",
                "team": "alpine",
                "car": 10,
            },
            {
                "ref": "esteban_ocon",
                "code": "OCO",
                "number": 31,
                "first": "Esteban",
                "last": "Ocon",
                "dob": date(1996, 9, 17),
                "nat": "French",
                "cc": "FRA",
                "team": "alpine",
                "car": 31,
            },
            # Williams
            {
                "ref": "alexander_albon",
                "code": "ALB",
                "number": 23,
                "first": "Alexander",
                "last": "Albon",
                "dob": date(1996, 3, 23),
                "nat": "Thai",
                "cc": "THA",
                "team": "williams",
                "car": 23,
            },
            {
                "ref": "logan_sargeant",
                "code": "SAR",
                "number": 2,
                "first": "Logan",
                "last": "Sargeant",
                "dob": date(2000, 12, 31),
                "nat": "American",
                "cc": "USA",
                "team": "williams",
                "car": 2,
            },
            # RB
            {
                "ref": "yuki_tsunoda",
                "code": "TSU",
                "number": 22,
                "first": "Yuki",
                "last": "Tsunoda",
                "dob": date(2000, 5, 11),
                "nat": "Japanese",
                "cc": "JPN",
                "team": "rb",
                "car": 22,
            },
            {
                "ref": "daniel_ricciardo",
                "code": "RIC",
                "number": 3,
                "first": "Daniel",
                "last": "Ricciardo",
                "dob": date(1989, 7, 1),
                "nat": "Australian",
                "cc": "AUS",
                "team": "rb",
                "car": 3,
            },
            # Kick Sauber
            {
                "ref": "valtteri_bottas",
                "code": "BOT",
                "number": 77,
                "first": "Valtteri",
                "last": "Bottas",
                "dob": date(1989, 8, 28),
                "nat": "Finnish",
                "cc": "FIN",
                "team": "kick_sauber",
                "car": 77,
            },
            {
                "ref": "guanyu_zhou",
                "code": "ZHO",
                "number": 24,
                "first": "Guanyu",
                "last": "Zhou",
                "dob": date(1999, 5, 30),
                "nat": "Chinese",
                "cc": "CHN",
                "team": "kick_sauber",
                "car": 24,
            },
            # Haas
            {
                "ref": "nico_hulkenberg",
                "code": "HUL",
                "number": 27,
                "first": "Nico",
                "last": "Hülkenberg",
                "dob": date(1987, 8, 19),
                "nat": "German",
                "cc": "DEU",
                "team": "haas",
                "car": 27,
            },
            {
                "ref": "kevin_magnussen",
                "code": "MAG",
                "number": 20,
                "first": "Kevin",
                "last": "Magnussen",
                "dob": date(1992, 10, 5),
                "nat": "Danish",
                "cc": "DNK",
                "team": "haas",
                "car": 20,
            },
        ]

        drivers: dict[str, Driver] = {}
        entries: dict[str, Entry] = {}
        for d_data in drivers_data:
            driver, _ = get_or_create(
                db,
                Driver,
                ref=d_data["ref"],
                defaults={
                    "code": d_data["code"],
                    "permanent_number": d_data["number"],
                    "first_name": d_data["first"],
                    "last_name": d_data["last"],
                    "date_of_birth": d_data["dob"],
                    "nationality": d_data["nat"],
                    "country_code": d_data["cc"],
                },
            )
            drivers[d_data["ref"]] = driver

            # Create entry (lineup)
            entry, _ = get_or_create(
                db,
                Entry,
                season_id=season.id,
                driver_id=driver.id,
                team_id=teams[d_data["team"]].id,
                defaults={"car_number": d_data["car"]},
            )
            entries[d_data["ref"]] = entry

        # === CIRCUITS ===
        circuits_data: list[CircuitData] = [
            {
                "ref": "sakhir",
                "name": "Bahrain International Circuit",
                "cc": "BHR",
                "city": "Sakhir",
            },
            {"ref": "jeddah", "name": "Jeddah Corniche Circuit", "cc": "SAU", "city": "Jeddah"},
            {"ref": "melbourne", "name": "Albert Park Circuit", "cc": "AUS", "city": "Melbourne"},
            {
                "ref": "suzuka",
                "name": "Suzuka International Racing Course",
                "cc": "JPN",
                "city": "Suzuka",
            },
            {
                "ref": "shanghai",
                "name": "Shanghai International Circuit",
                "cc": "CHN",
                "city": "Shanghai",
            },
            {"ref": "miami", "name": "Miami International Autodrome", "cc": "USA", "city": "Miami"},
        ]

        circuits: dict[str, Circuit] = {}
        for c_data in circuits_data:
            circuit, _ = get_or_create(
                db,
                Circuit,
                ref=c_data["ref"],
                defaults={
                    "name": c_data["name"],
                    "country_code": c_data["cc"],
                    "city": c_data["city"],
                },
            )
            circuits[c_data["ref"]] = circuit

        # === EVENTS & RACE RESULTS ===
        # Realistic 2024 season results (simplified)
        races_data: list[RaceData] = [
            {
                "round": 1,
                "circuit": "sakhir",
                "name": "Bahrain Grand Prix",
                "date": datetime(2024, 3, 2, 18, 0, 0),
                "results": [
                    ("max_verstappen", 1, 25, "FINISHED", 57, 1),
                    ("sergio_perez", 2, 18, "FINISHED", 57, 2),
                    ("carlos_sainz", 3, 15, "FINISHED", 57, 3),
                    ("charles_leclerc", 4, 12, "FINISHED", 57, 4),
                    ("george_russell", 5, 10, "FINISHED", 57, 5),
                    ("lewis_hamilton", 6, 8, "FINISHED", 57, 6),
                    ("lando_norris", 7, 6, "FINISHED", 57, 7),
                    ("oscar_piastri", 8, 4, "FINISHED", 57, 8),
                    ("fernando_alonso", 9, 2, "FINISHED", 57, 9),
                    ("lance_stroll", 10, 1, "FINISHED", 57, 10),
                ],
            },
            {
                "round": 2,
                "circuit": "jeddah",
                "name": "Saudi Arabian Grand Prix",
                "date": datetime(2024, 3, 9, 20, 0, 0),
                "results": [
                    ("max_verstappen", 1, 25, "FINISHED", 50, 1),
                    ("sergio_perez", 2, 18, "FINISHED", 50, 2),
                    ("charles_leclerc", 3, 15, "FINISHED", 50, 3),
                    ("oscar_piastri", 4, 12, "FINISHED", 50, 5),
                    ("fernando_alonso", 5, 10, "FINISHED", 50, 4),
                    ("george_russell", 6, 8, "FINISHED", 50, 6),
                    ("lewis_hamilton", 7, 6, "FINISHED", 50, 7),
                    ("lando_norris", 8, 4, "FINISHED", 50, 8),
                    ("yuki_tsunoda", 9, 2, "FINISHED", 50, 11),
                    ("lance_stroll", 10, 1, "FINISHED", 50, 9),
                ],
            },
            {
                "round": 3,
                "circuit": "melbourne",
                "name": "Australian Grand Prix",
                "date": datetime(2024, 3, 24, 15, 0, 0),
                "results": [
                    ("carlos_sainz", 1, 25, "FINISHED", 58, 5),
                    ("charles_leclerc", 2, 18, "FINISHED", 58, 3),
                    ("lando_norris", 3, 15, "FINISHED", 58, 4),
                    ("oscar_piastri", 4, 12, "FINISHED", 58, 6),
                    ("sergio_perez", 5, 10, "FINISHED", 58, 2),
                    ("lewis_hamilton", 6, 8, "FINISHED", 58, 8),
                    ("george_russell", 7, 6, "FINISHED", 58, 7),
                    ("yuki_tsunoda", 8, 4, "FINISHED", 58, 9),
                    ("fernando_alonso", 9, 2, "FINISHED", 58, 10),
                    ("alexander_albon", 10, 1, "FINISHED", 58, 11),
                    ("max_verstappen", None, 0, "DNF", 0, 1),  # Brake failure
                ],
            },
            {
                "round": 4,
                "circuit": "suzuka",
                "name": "Japanese Grand Prix",
                "date": datetime(2024, 4, 7, 14, 0, 0),
                "results": [
                    ("max_verstappen", 1, 25, "FINISHED", 53, 1),
                    ("sergio_perez", 2, 18, "FINISHED", 53, 2),
                    ("carlos_sainz", 3, 15, "FINISHED", 53, 3),
                    ("charles_leclerc", 4, 12, "FINISHED", 53, 5),
                    ("lando_norris", 5, 10, "FINISHED", 53, 4),
                    ("fernando_alonso", 6, 8, "FINISHED", 53, 7),
                    ("george_russell", 7, 6, "FINISHED", 53, 6),
                    ("oscar_piastri", 8, 4, "FINISHED", 53, 9),
                    ("lewis_hamilton", 9, 2, "FINISHED", 53, 8),
                    ("yuki_tsunoda", 10, 1, "FINISHED", 53, 10),
                ],
            },
            {
                "round": 5,
                "circuit": "shanghai",
                "name": "Chinese Grand Prix",
                "date": datetime(2024, 4, 21, 15, 0, 0),
                "results": [
                    ("max_verstappen", 1, 25, "FINISHED", 56, 1),
                    ("lando_norris", 2, 18, "FINISHED", 56, 4),
                    ("sergio_perez", 3, 15, "FINISHED", 56, 2),
                    ("charles_leclerc", 4, 12, "FINISHED", 56, 6),
                    ("carlos_sainz", 5, 10, "FINISHED", 56, 3),
                    ("george_russell", 6, 8, "FINISHED", 56, 5),
                    ("fernando_alonso", 7, 6, "FINISHED", 56, 7),
                    ("lewis_hamilton", 8, 4, "FINISHED", 56, 9),
                    ("oscar_piastri", 9, 2, "FINISHED", 56, 8),
                    ("nico_hulkenberg", 10, 1, "FINISHED", 56, 10),
                ],
            },
            {
                "round": 6,
                "circuit": "miami",
                "name": "Miami Grand Prix",
                "date": datetime(2024, 5, 5, 20, 30, 0),
                "results": [
                    ("lando_norris", 1, 25, "FINISHED", 57, 5),
                    ("max_verstappen", 2, 18, "FINISHED", 57, 2),
                    ("charles_leclerc", 3, 15, "FINISHED", 57, 3),
                    ("sergio_perez", 4, 12, "FINISHED", 57, 1),
                    ("carlos_sainz", 5, 10, "FINISHED", 57, 4),
                    ("lewis_hamilton", 6, 8, "FINISHED", 57, 7),
                    ("yuki_tsunoda", 7, 6, "FINISHED", 57, 9),
                    ("oscar_piastri", 8, 4, "FINISHED", 57, 6),
                    ("nico_hulkenberg", 9, 2, "FINISHED", 57, 11),
                    ("esteban_ocon", 10, 1, "FINISHED", 57, 12),
                ],
            },
        ]

        for race_data in races_data:
            # Create event
            event, _ = get_or_create(
                db,
                Event,
                season_id=season.id,
                circuit_id=circuits[race_data["circuit"]].id,
                round=race_data["round"],
                defaults={"name": race_data["name"]},
            )

            # Create sessions (FP, Q, Race)
            _fp_session, _ = get_or_create(
                db,
                RaceSession,
                event_id=event.id,
                type=SessionType.FP,
                session_order=1,
                defaults={"name": "Practice", "started_at": race_data["date"]},
            )
            _q_session, _ = get_or_create(
                db,
                RaceSession,
                event_id=event.id,
                type=SessionType.QUALIFYING,
                session_order=2,
                defaults={"name": "Qualifying", "started_at": race_data["date"]},
            )
            race_session, _ = get_or_create(
                db,
                RaceSession,
                event_id=event.id,
                type=SessionType.RACE,
                session_order=3,
                defaults={"name": "Race", "started_at": race_data["date"]},
            )

            # Create race results
            for driver_ref, position, points, status, laps, grid in race_data["results"]:
                get_or_create(
                    db,
                    SessionResult,
                    session_id=race_session.id,
                    entry_id=entries[driver_ref].id,
                    defaults={
                        "position": position,
                        "points": points,
                        "status": status,
                        "laps": laps,
                        "grid": grid,
                        "classified": status == "FINISHED",
                    },
                )

        db.commit()
        print("✅ Comprehensive 2024 season data seeded successfully!")
        print("   - 10 teams")
        print("   - 20 drivers")
        print("   - 6 circuits")
        print("   - 6 races with results")

    except Exception as e:
        print(f"❌ Seed failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


# Legacy alias for backward compatibility
def seed_minimal_2024() -> None:
    """Alias for backward compatibility."""
    seed_comprehensive_2024()


if __name__ == "__main__":
    seed_comprehensive_2024()
