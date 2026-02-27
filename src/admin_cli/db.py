from contextlib import contextmanager
import psycopg
from psycopg.rows import dict_row
from .config import Settings


def dsn(s: Settings) -> str:
    return (
        f"host={s.db_host} port={s.db_port} dbname={s.db_name} "
        f"user={s.db_user} password={s.db_password} sslmode={s.db_sslmode}"
    )


@contextmanager
def get_conn(s: Settings):
    conn = psycopg.connect(dsn(s), row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.close()


def fetch_one(conn, sql: str, params: dict | None = None):
    with conn.cursor() as cur:
        cur.execute(sql, params or {})
        return cur.fetchone()


def fetch_all(conn, sql: str, params: dict | None = None):
    with conn.cursor() as cur:
        cur.execute(sql, params or {})
        return cur.fetchall()


def execute(conn, sql: str, params: dict | None = None) -> int:
    with conn.cursor() as cur:
        cur.execute(sql, params or {})
        return cur.rowcount
