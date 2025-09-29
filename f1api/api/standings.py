from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from f1api.core.db import get_db
from f1api.models import Driver, Entry, Season, SessionResult, SessionType, Team
from f1api.models import Session as RaceSession
from f1api.schemas import ConstructorStandingRead, DriverStandingRead

router = APIRouter(prefix="/standings", tags=["Standings"])


@router.get("/drivers", response_model=list[DriverStandingRead])
def get_driver_standings(
    db: Session = Depends(get_db),  # noqa: B008
    season_year: int = Query(..., description="Season year (required)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
) -> list[DriverStandingRead]:
    """
    Get driver championship standings for a season.
    Points are aggregated from all race sessions.
    """
    # Verify season exists
    season = db.scalar(select(Season).filter(Season.year == season_year))
    if not season:
        raise HTTPException(status_code=404, detail=f"Season {season_year} not found")

    # Aggregate points and wins per driver
    # Join: SessionResult -> Entry -> Driver/Team -> Session (filter RACE only)
    stmt = (
        select(
            Driver.id.label("driver_id"),
            Driver.ref.label("driver_ref"),
            Driver.code.label("driver_code"),
            Driver.first_name.label("driver_first_name"),
            Driver.last_name.label("driver_last_name"),
            Team.id.label("team_id"),
            Team.name.label("team_name"),
            func.sum(SessionResult.points).label("points"),
            func.count(func.nullif(SessionResult.position != 1, True)).label("wins"),
        )
        .select_from(SessionResult)
        .join(SessionResult.entry)
        .join(Entry.driver)
        .join(Entry.team)
        .join(SessionResult.session)
        .filter(Entry.season_id == season.id)
        .filter(RaceSession.type == SessionType.RACE)
        .group_by(Driver.id, Team.id)
        .order_by(func.sum(SessionResult.points).desc(), Driver.last_name)
        .limit(limit)
        .offset(offset)
    )

    rows = db.execute(stmt).all()

    # Build response with positions
    standings = []
    for idx, row in enumerate(rows, start=1 + offset):
        standings.append(
            DriverStandingRead(
                position=idx,
                driver_id=row.driver_id,
                driver_ref=row.driver_ref,
                driver_code=row.driver_code,
                driver_first_name=row.driver_first_name,
                driver_last_name=row.driver_last_name,
                team_id=row.team_id,
                team_name=row.team_name,
                points=float(row.points or 0),
                wins=int(row.wins or 0),
            )
        )

    return standings


@router.get("/constructors", response_model=list[ConstructorStandingRead])
def get_constructor_standings(
    db: Session = Depends(get_db),  # noqa: B008
    season_year: int = Query(..., description="Season year (required)"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
) -> list[ConstructorStandingRead]:
    """
    Get constructor (team) championship standings for a season.
    Points are aggregated from all drivers' race results.
    """
    # Verify season exists
    season = db.scalar(select(Season).filter(Season.year == season_year))
    if not season:
        raise HTTPException(status_code=404, detail=f"Season {season_year} not found")

    # Aggregate points and wins per team
    stmt = (
        select(
            Team.id.label("team_id"),
            Team.ref.label("team_ref"),
            Team.name.label("team_name"),
            func.sum(SessionResult.points).label("points"),
            func.count(func.nullif(SessionResult.position != 1, True)).label("wins"),
        )
        .select_from(SessionResult)
        .join(SessionResult.entry)
        .join(Entry.team)
        .join(SessionResult.session)
        .filter(Entry.season_id == season.id)
        .filter(RaceSession.type == SessionType.RACE)
        .group_by(Team.id)
        .order_by(func.sum(SessionResult.points).desc(), Team.name)
        .limit(limit)
        .offset(offset)
    )

    rows = db.execute(stmt).all()

    # Build response with positions
    standings = []
    for idx, row in enumerate(rows, start=1 + offset):
        standings.append(
            ConstructorStandingRead(
                position=idx,
                team_id=row.team_id,
                team_ref=row.team_ref,
                team_name=row.team_name,
                points=float(row.points or 0),
                wins=int(row.wins or 0),
            )
        )

    return standings
