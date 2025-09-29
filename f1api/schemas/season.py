from pydantic import BaseModel


class SeasonRead(BaseModel):
    id: int
    year: int
