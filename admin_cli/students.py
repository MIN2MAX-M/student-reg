from __future__ import annotations

from typing import Optional

import psycopg
from psycopg.errors import UniqueViolation

from .db import fetch_all, fetch_one, execute


def _norm_text(s: Optional[str]) -> Optional[str]:
    if s is None:
        return None
    s = s.strip()
    return s if s else None


def _norm_email(email: Optional[str]) -> Optional[str]:
    email = _norm_text(email)
    if email is None:
        return None
    return email.lower()


def list_students(conn, limit: int, offset: int):
    return fetch_all(
        conn,
        """
        SELECT id, first_name, last_name, email, created_at, updated_at
        FROM students
        ORDER BY id
        LIMIT %(limit)s OFFSET %(offset)s
        """,
        {"limit": limit, "offset": offset},
    )


def search_students(conn, q: str, limit: int, offset: int):
    like = f"%{q}%"
    return fetch_all(
        conn,
        """
        SELECT id, first_name, last_name, email, created_at, updated_at
        FROM students
        WHERE first_name ILIKE %(like)s
           OR last_name  ILIKE %(like)s
           OR email      ILIKE %(like)s
        ORDER BY id
        LIMIT %(limit)s OFFSET %(offset)s
        """,
        {"like": like, "limit": limit, "offset": offset},
    )


def get_student(conn, student_id: int):
    return fetch_one(
        conn,
        """
        SELECT id, first_name, last_name, email, created_at, updated_at
        FROM students
        WHERE id = %(id)s
        """,
        {"id": student_id},
    )


def create_student(conn, first_name: str, last_name: str, email: str):
    first_name = _norm_text(first_name) or ""
    last_name = _norm_text(last_name) or ""
    email = _norm_email(email) or ""

    try:
        row = fetch_one(
            conn,
            """
            INSERT INTO students(first_name, last_name, email)
            VALUES (%(first)s, %(last)s, %(email)s)
            RETURNING id, first_name, last_name, email, created_at, updated_at
            """,
            {"first": first_name, "last": last_name, "email": email},
        )
        return row
    except UniqueViolation as e:
        # Friendly error for duplicate email if you have UNIQUE(email)
        raise ValueError(f"Email already exists: {email}") from e


def update_student(
    conn,
    student_id: int,
    first_name: Optional[str],
    last_name: Optional[str],
    email: Optional[str],
):
    # Normalize inputs
    first_name = _norm_text(first_name)
    last_name = _norm_text(last_name)
    email = _norm_email(email)

    # No-op guard (optional but nice)
    if first_name is None and last_name is None and email is None:
        # Caller (CLI) already guards this in dry-run, but keep it safe here too.
        return get_student(conn, student_id)

    try:
        row = fetch_one(
            conn,
            """
            UPDATE students
            SET
              first_name = COALESCE(%(first)s, first_name),
              last_name  = COALESCE(%(last)s, last_name),
              email      = COALESCE(%(email)s, email)
            WHERE id = %(id)s
            RETURNING id, first_name, last_name, email, created_at, updated_at
            """,
            {"id": student_id, "first": first_name, "last": last_name, "email": email},
        )
        return row
    except UniqueViolation as e:
        raise ValueError(f"Email already exists: {email}") from e


def delete_student(conn, student_id: int) -> int:
    return execute(conn, "DELETE FROM students WHERE id = %(id)s", {"id": student_id})
