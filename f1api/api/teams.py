from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from f1api.core.db import get_db
from f1api.models import Team
from f1api.schemas import PaginatedResponse, TeamRead

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("", response_model=PaginatedResponse[TeamRead])
def list_teams(
    db: Session = Depends(get_db),  # noqa: B008
    ref: str | None = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
) -> PaginatedResponse[TeamRead]:
    # Build base query
    stmt = select(Team)
    if ref:
        stmt = stmt.filter(Team.ref == ref)

    # Get total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.scalar(count_stmt) or 0

    # Get paginated items
    stmt = stmt.order_by(Team.name).limit(limit).offset(offset)
    teams = db.scalars(stmt).all()
    items = [TeamRead.model_validate(t) for t in teams]

    return PaginatedResponse.create(items=items, total=total, limit=limit, offset=offset)


@router.get("/{team_id}", response_model=TeamRead)
def get_team(team_id: int, db: Session = Depends(get_db)) -> TeamRead:  # noqa: B008
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamRead.model_validate(team)
