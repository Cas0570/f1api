from datetime import date
from pydantic import BaseModel


class DriverRead(BaseModel):
    id: int
    ref: str
    code: str | None
    permanent_number: int | None
    first_name: str
    last_name: str
    date_of_birth: date
    nationality: str | None
    country_code: str | None
