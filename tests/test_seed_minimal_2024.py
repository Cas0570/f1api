import os

import pytest
from sqlalchemy import create_engine, text


@pytest.mark.skipif(
    not os.getenv("DATABASE_URL"),
    reason="DATABASE_URL not set; skipping seed test",
)
def test_seed_inserts_entities() -> None:
    engine = create_engine(os.environ["DATABASE_URL"])
    with engine.begin() as conn:
        # season exists
        year = conn.execute(text("SELECT year FROM seasons WHERE year=2024")).scalar_one()
        assert year == 2024

        # team + drivers exist
        tcount = conn.execute(
            text("SELECT count(*) FROM teams WHERE ref='red_bull_racing'")
        ).scalar_one()
        assert tcount == 1
        dcount = conn.execute(
            text("SELECT count(*) FROM drivers WHERE ref in ('max_verstappen','sergio_perez')")
        ).scalar_one()
        assert dcount == 2

        # event + sessions exist
        ev_id = conn.execute(
            text(
                "SELECT e.id FROM events e "
                "JOIN seasons s ON e.season_id = s.id "
                "WHERE s.year = 2024 AND e.round = 1"
            )
        ).scalar_one()
        scount = conn.execute(
            text("SELECT count(*) FROM sessions WHERE event_id=:eid"),
            {"eid": ev_id},
        ).scalar_one()
        assert scount >= 3

        # race results have 1st and 2nd
        rcount = conn.execute(
            text(
                """
                SELECT count(*)
                FROM session_results r
                JOIN sessions s ON r.session_id = s.id
                WHERE s.event_id=:eid AND s.type='RACE' AND r.position in (1,2)
            """
            ),
            {"eid": ev_id},
        ).scalar_one()
        assert rcount == 2
