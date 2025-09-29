from f1api.models.base import Base

# Import models so Alembic autogenerate can see them
from f1api.models.season import Season

__all__ = ["Base", "Season"]
