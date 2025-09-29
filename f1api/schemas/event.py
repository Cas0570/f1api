from pydantic import BaseModel


class EventRead(BaseModel):
    id: int
    season_id: int
    circuit_id: int
    round: int
    name: str
