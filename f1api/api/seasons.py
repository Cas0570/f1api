from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from f1api.core.db import get_db
from f1api.models import Season
from f1api.schemas import PaginatedResponse, SeasonRead

router = APIRouter(prefix="/seasons", tags=["Seasons"])


@router.get("", response_model=PaginatedResponse[SeasonRead])
def list_seasons(
    db: Session = Depends(get_db),  # noqa: B008
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
) -> PaginatedResponse[SeasonRead]:
    # Get total count
    total = db.scalar(select(func.count()).select_from(Season)) or 0

    # Get paginated items
    stmt = select(Season).order_by(Season.year).limit(limit).offset(offset)
    seasons = db.scalars(stmt).all()
    items = [SeasonRead.model_validate(s) for s in seasons]

    return PaginatedResponse.create(items=items, total=total, limit=limit, offset=offset)


@router.get("/{season_id}", response_model=SeasonRead)
def get_season(season_id: int, db: Session = Depends(get_db)) -> SeasonRead:  # noqa: B008
    season = db.get(Season, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return SeasonRead.model_validate(season)
