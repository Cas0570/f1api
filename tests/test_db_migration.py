import os

import pytest
from sqlalchemy import text
from sqlalchemy.engine import create_engine


@pytest.mark.skipif(
    not os.getenv("DATABASE_URL"),
    reason="DATABASE_URL not set; skipping DB migration test",
)
def test_seasons_table_exists() -> None:
    engine = create_engine(os.environ["DATABASE_URL"])
    with engine.connect() as conn:
        res = conn.execute(
            text("SELECT column_name FROM information_schema.columns WHERE table_name='seasons'")
        )
        columns = {row[0] for row in res.fetchall()}
    assert {"id", "year", "created_at"}.issubset(columns)
