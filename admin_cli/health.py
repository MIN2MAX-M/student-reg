from .db import fetch_one

def db_status(conn):
    return fetch_one(
        conn,
        """
        SELECT
          current_database() AS db,
          current_user AS user,
          inet_server_addr()::text AS server_addr,
          inet_server_port() AS server_port,
          version() AS version
        """
    )

def permissions_check(conn):
    # Checks whether current role can CREATE TABLE in public schema (should be FALSE for app_user)
    return fetch_one(
        conn,
        """
        SELECT
          has_database_privilege(current_user, current_database(), 'CONNECT') AS can_connect,
          has_schema_privilege(current_user, 'public', 'USAGE') AS schema_usage,
          has_schema_privilege(current_user, 'public', 'CREATE') AS schema_create,
          has_table_privilege(current_user, 'public.students', 'SELECT,INSERT,UPDATE,DELETE') AS students_crud
        """
    )

def seed_status(conn):
    # simple demo: count students; adjust if you tag seed rows
    return fetch_one(conn, "SELECT COUNT(*)::int AS student_count FROM students")
