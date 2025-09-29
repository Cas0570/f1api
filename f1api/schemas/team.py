from pydantic import BaseModel


class TeamRead(BaseModel):
    id: int
    ref: str
    name: str
