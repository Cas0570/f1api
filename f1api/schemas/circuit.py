from pydantic import BaseModel, ConfigDict


class CircuitRead(BaseModel):
    id: int
    ref: str
    name: str
    country_code: str | None
    city: str | None

    model_config = ConfigDict(from_attributes=True)
