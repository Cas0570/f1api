from __future__ import annotations
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from f1api.models.base import Base, TimestampMixin


class SessionResult(Base, TimestampMixin):
    __tablename__ = "session_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False
    )
    entry_id: Mapped[int] = mapped_column(
        ForeignKey("entries.id", ondelete="CASCADE"), nullable=False
    )

    position: Mapped[int | None] = mapped_column(nullable=True)  # finishing position (1..)
    points: Mapped[float] = mapped_column(nullable=False, default=0.0)
    status: Mapped[str | None] = mapped_column(nullable=True)  # e.g. FINISHED, DNF
    time_ms: Mapped[int | None] = mapped_column(nullable=True)  # total race time in ms (optional)
    gap_ms: Mapped[int | None] = mapped_column(nullable=True)  # gap to winner in ms
    laps: Mapped[int | None] = mapped_column(nullable=True)
    grid: Mapped[int | None] = mapped_column(nullable=True)
    classified: Mapped[bool] = mapped_column(nullable=False, default=True)

    __table_args__ = (
        Index("ix_results_session", "session_id"),
        Index("ix_results_session_pos", "session_id", "position"),
    )

    session = relationship("Session", back_populates="results")
    entry = relationship("Entry", back_populates="results")
