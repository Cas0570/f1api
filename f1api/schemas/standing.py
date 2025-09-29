from pydantic import BaseModel, ConfigDict


class DriverStandingRead(BaseModel):
    """Driver championship standing."""

    position: int
    driver_id: int
    driver_ref: str
    driver_code: str | None
    driver_first_name: str
    driver_last_name: str
    team_id: int
    team_name: str
    points: float
    wins: int

    model_config = ConfigDict(from_attributes=True)


class ConstructorStandingRead(BaseModel):
    """Constructor (team) championship standing."""

    position: int
    team_id: int
    team_ref: str
    team_name: str
    points: float
    wins: int

    model_config = ConfigDict(from_attributes=True)
