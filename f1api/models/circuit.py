from __future__ import annotations
from sqlalchemy import String, UniqueConstraint, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from f1api.models.base import Base, TimestampMixin


class Circuit(Base, TimestampMixin):
    __tablename__ = "circuits"

    id: Mapped[int] = mapped_column(primary_key=True)
    ref: Mapped[str] = mapped_column(String(64), nullable=False)  # "sakhir"
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(3), nullable=True)
    city: Mapped[str | None] = mapped_column(String(64), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (UniqueConstraint("ref", name="uq_circuits_ref"),)

    events = relationship("Event", back_populates="circuit")
