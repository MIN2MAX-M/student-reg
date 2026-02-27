from .db import fetch_one, fetch_all


def flyway_info(conn):
    # Flyway schema history table is usually: flyway_schema_history
    # If yours uses a custom name/schema, we’ll adjust.
    latest = fetch_one(
        conn,
        """
        SELECT installed_rank, version, description, type, script, installed_on, success
        FROM flyway_schema_history
        ORDER BY installed_rank DESC
        LIMIT 1
        """,
    )
    counts = fetch_one(
        conn,
        """
        SELECT
          SUM(CASE WHEN success THEN 1 ELSE 0 END) AS successful,
          SUM(CASE WHEN success THEN 0 ELSE 1 END) AS failed,
          COUNT(*) AS total
        FROM flyway_schema_history
        """,
    )
    return {"latest": latest, "counts": counts}


def flyway_recent(conn, n: int = 10):
    return fetch_all(
        conn,
        """
        SELECT installed_rank, version, description, installed_on, success
        FROM flyway_schema_history
        ORDER BY installed_rank DESC
        LIMIT %(n)s
        """,
        {"n": n},
    )
