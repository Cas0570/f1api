from pydantic import BaseModel, ConfigDict


class SeasonRead(BaseModel):
    id: int
    year: int

    model_config = ConfigDict(from_attributes=True)
