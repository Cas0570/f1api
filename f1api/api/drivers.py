from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from f1api.core.db import get_db
from f1api.models import Driver
from f1api.schemas import DriverRead, PaginatedResponse

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.get("", response_model=PaginatedResponse[DriverRead])
def list_drivers(
    db: Session = Depends(get_db),  # noqa: B008
    ref: str | None = None,
    code: str | None = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
) -> PaginatedResponse[DriverRead]:
    # Build base query
    stmt = select(Driver)
    if ref:
        stmt = stmt.filter(Driver.ref == ref)
    if code:
        stmt = stmt.filter(Driver.code == code)

    # Get total count (before limit/offset)
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.scalar(count_stmt) or 0

    # Get paginated items
    stmt = stmt.order_by(Driver.last_name, Driver.first_name).limit(limit).offset(offset)
    drivers = db.scalars(stmt).all()
    items = [DriverRead.model_validate(d) for d in drivers]

    return PaginatedResponse.create(items=items, total=total, limit=limit, offset=offset)


@router.get("/{driver_id}", response_model=DriverRead)
def get_driver(driver_id: int, db: Session = Depends(get_db)) -> DriverRead:  # noqa: B008
    driver = db.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return DriverRead.model_validate(driver)
