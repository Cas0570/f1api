from pydantic import BaseModel, ConfigDict


class TeamRead(BaseModel):
    id: int
    ref: str
    name: str

    model_config = ConfigDict(from_attributes=True)
