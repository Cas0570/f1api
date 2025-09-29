from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from f1api.core.db import get_db
from f1api.models import Event, Season
from f1api.schemas import EventRead

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=list[EventRead])
def list_events(
    db: Session = Depends(get_db),  # noqa: B008
    season_year: int | None = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
) -> list[EventRead]:
    stmt = select(Event)
    if season_year:
        stmt = stmt.join(Event.season).filter(Season.year == season_year)
    stmt = stmt.order_by(Event.round).limit(limit).offset(offset)
    events = db.scalars(stmt).all()
    return [EventRead.model_validate(e) for e in events]


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)) -> EventRead:  # noqa: B008
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventRead.model_validate(event)
