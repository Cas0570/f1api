from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from f1api.models.base import Base, TimestampMixin


class SessionType(StrEnum):
    FP = "FP"  # practice (we can extend to FP1/FP2 later via name/sequence)
    QUALIFYING = "Q"
    RACE = "RACE"


class Session(Base, TimestampMixin):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )

    type: Mapped[SessionType] = mapped_column(
        SAEnum(SessionType, name="session_type"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    session_order: Mapped[int] = mapped_column(nullable=False, default=1)  # FP=1, Q=2, Race=3
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (Index("ix_sessions_event", "event_id"),)

    event = relationship("Event", back_populates="sessions")
    results = relationship("SessionResult", back_populates="session", cascade="all, delete-orphan")
