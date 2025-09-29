from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from f1api.api.deps import get_db
from f1api.models import Season
from f1api.schemas import SeasonRead

router = APIRouter(prefix="/seasons", tags=["Seasons"])


@router.get("", response_model=list[SeasonRead])
def list_seasons(
    db: Session = Depends(get_db),  # noqa: B008
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    stmt = select(Season).order_by(Season.year).limit(limit).offset(offset)
    return db.scalars(stmt).all()


@router.get("/{season_id}", response_model=SeasonRead)
def get_season(season_id: int, db: Session = Depends(get_db)):  # noqa: B008
    season = db.get(Season, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season
