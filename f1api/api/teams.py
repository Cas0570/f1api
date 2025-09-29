from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from f1api.api.deps import get_db
from f1api.models import Team
from f1api.schemas import TeamRead

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("", response_model=list[TeamRead])
def list_teams(
    db: Session = Depends(get_db),  # noqa: B008
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    stmt = select(Team).order_by(Team.name).limit(limit).offset(offset)
    return db.scalars(stmt).all()


@router.get("/{team_id}", response_model=TeamRead)
def get_team(team_id: int, db: Session = Depends(get_db)):  # noqa: B008
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team
