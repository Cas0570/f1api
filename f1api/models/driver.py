from __future__ import annotations

from datetime import date

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from f1api.models.base import Base, TimestampMixin


class Driver(Base, TimestampMixin):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    ref: Mapped[str] = mapped_column(String(64), nullable=False)  # "max_verstappen"
    code: Mapped[str | None] = mapped_column(String(3), nullable=True)  # "VER"
    permanent_number: Mapped[int | None] = mapped_column(nullable=True)

    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(nullable=False)

    nationality: Mapped[str | None] = mapped_column(String(64), nullable=True)
    country_code: Mapped[str | None] = mapped_column(String(3), nullable=True)
    place_of_birth_city: Mapped[str | None] = mapped_column(String(64), nullable=True)
    place_of_birth_country_code: Mapped[str | None] = mapped_column(String(3), nullable=True)

    wikipedia_url: Mapped[str | None] = mapped_column(String(256), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(256), nullable=True)

    __table_args__ = (UniqueConstraint("ref", name="uq_drivers_ref"),)

    entries = relationship("Entry", back_populates="driver", cascade="all, delete-orphan")
