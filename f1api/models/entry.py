from __future__ import annotations

from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from f1api.models.base import Base, TimestampMixin


class Entry(Base, TimestampMixin):
    """
    A driver racing for a team in a given season (line-up).
    """

    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"), nullable=False)

    car_number: Mapped[int | None] = mapped_column(nullable=True)

    __table_args__ = (
        UniqueConstraint("season_id", "driver_id", name="uq_entries_season_driver"),
        UniqueConstraint("season_id", "team_id", "driver_id", name="uq_entries_season_team_driver"),
        Index("ix_entries_season", "season_id"),
    )

    season = relationship("Season", back_populates="entries")
    team = relationship("Team", back_populates="entries")
    driver = relationship("Driver", back_populates="entries")
    results = relationship("SessionResult", back_populates="entry", cascade="all, delete-orphan")
