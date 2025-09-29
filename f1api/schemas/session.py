from datetime import datetime
from pydantic import BaseModel


class SessionRead(BaseModel):
    id: int
    event_id: int
    type: str
    name: str
    session_order: int
    started_at: datetime | None
