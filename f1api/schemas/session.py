from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SessionRead(BaseModel):
    id: int
    event_id: int
    type: str
    name: str
    session_order: int
    started_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
