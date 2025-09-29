from __future__ import annotations

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from f1api.models.base import Base, TimestampMixin


class Event(Base, TimestampMixin):
    """
    A Grand Prix within a season, linked to a circuit.
    """

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id", ondelete="CASCADE"), nullable=False
    )
    circuit_id: Mapped[int] = mapped_column(ForeignKey("circuits.id"), nullable=False)

    round: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)

    __table_args__ = (
        UniqueConstraint("season_id", "round", name="uq_events_season_round"),
        Index("ix_events_season", "season_id"),
    )

    season = relationship("Season", back_populates="events")
    circuit = relationship("Circuit", back_populates="events")
    sessions = relationship("Session", back_populates="event", cascade="all, delete-orphan")
