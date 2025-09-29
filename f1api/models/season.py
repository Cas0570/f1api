from __future__ import annotations

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from f1api.models.base import Base, TimestampMixin


class Season(Base, TimestampMixin):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (UniqueConstraint("year", name="uq_seasons_year"),)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Season year={self.year}>"
