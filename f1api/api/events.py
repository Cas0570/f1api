from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from f1api.core.db import get_db
from f1api.models import Event, Season
from f1api.schemas import EventRead, PaginatedResponse

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=PaginatedResponse[EventRead])
def list_events(
    db: Session = Depends(get_db),  # noqa: B008
    season_year: int | None = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
) -> PaginatedResponse[EventRead]:
    # Build base query
    stmt = select(Event)
    if season_year:
        stmt = stmt.join(Event.season).filter(Season.year == season_year)

    # Get total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.scalar(count_stmt) or 0

    # Get paginated items
    stmt = stmt.order_by(Event.round).limit(limit).offset(offset)
    events = db.scalars(stmt).all()
    items = [EventRead.model_validate(e) for e in events]

    return PaginatedResponse.create(items=items, total=total, limit=limit, offset=offset)


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)) -> EventRead:  # noqa: B008
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventRead.model_validate(event)
