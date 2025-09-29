from pydantic import BaseModel


class CircuitRead(BaseModel):
    id: int
    ref: str
    name: str
    country_code: str | None
    city: str | None
