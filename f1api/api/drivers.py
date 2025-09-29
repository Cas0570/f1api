from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from f1api.core.db import get_db
from f1api.models import Driver
from f1api.schemas import DriverRead

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.get("", response_model=list[DriverRead])
def list_drivers(
    db: Session = Depends(get_db),  # noqa: B008
    ref: str | None = None,
    code: str | None = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
) -> list[DriverRead]:
    stmt = select(Driver)
    if ref:
        stmt = stmt.filter(Driver.ref == ref)
    if code:
        stmt = stmt.filter(Driver.code == code)
    stmt = stmt.order_by(Driver.last_name, Driver.first_name).limit(limit).offset(offset)
    drivers = db.scalars(stmt).all()
    return [DriverRead.model_validate(d) for d in drivers]


@router.get("/{driver_id}", response_model=DriverRead)
def get_driver(driver_id: int, db: Session = Depends(get_db)) -> DriverRead:  # noqa: B008
    driver = db.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return DriverRead.model_validate(driver)
