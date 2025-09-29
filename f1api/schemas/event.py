from pydantic import BaseModel, ConfigDict


class EventRead(BaseModel):
    id: int
    season_id: int
    circuit_id: int
    round: int
    name: str

    model_config = ConfigDict(from_attributes=True)
