from pydantic import BaseModel


class SessionResultRead(BaseModel):
    id: int
    session_id: int
    entry_id: int
    position: int | None
    points: float
    status: str | None
    laps: int | None
