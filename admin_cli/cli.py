import typer
from dotenv import load_dotenv
from rich.prompt import Confirm

from .config import load_settings
from .db import get_conn
from . import students as students_mod
from . import flyway as flyway_mod
from . import health as health_mod
from .util import console, render_table, render_kv

app = typer.Typer(no_args_is_help=True)
students = typer.Typer(no_args_is_help=True)
ops = typer.Typer(no_args_is_help=True)

app.add_typer(students, name="students")
app.add_typer(ops, name="ops")


@app.callback()
def main():
    """Admin CLI: safe operational interface (CRUD + ops checks)."""
    load_dotenv()  # optional, loads .env if present


# -----------------------
# Students commands
# -----------------------

@students.command("list")
def students_list(
    limit: int = typer.Option(20, "--limit", "-l", help="Max rows to return"),
    offset: int = typer.Option(0, "--offset", "-o", help="Rows to skip"),
):
    s = load_settings()
    with get_conn(s) as conn:
        rows = students_mod.list_students(conn, limit, offset)
    render_table(rows, f"Students (limit={limit}, offset={offset})")


@students.command("search")
def students_search(
    q: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(20, "--limit", "-l", help="Max rows to return"),
    offset: int = typer.Option(0, "--offset", "-o", help="Rows to skip"),
):
    s = load_settings()
    with get_conn(s) as conn:
        rows = students_mod.search_students(conn, q, limit, offset)
    render_table(rows, f"Search: {q} (limit={limit}, offset={offset})")


@students.command("get")
def students_get(student_id: int = typer.Argument(..., help="Student ID")):
    s = load_settings()
    with get_conn(s) as conn:
        row = students_mod.get_student(conn, student_id)
    render_kv(f"Student #{student_id}", row)


@students.command("create")
def students_create(
    first_name: str = typer.Argument(..., help="First name"),
    last_name: str = typer.Argument(..., help="Last name"),
    email: str = typer.Argument(..., help="Email address"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Don't write; only show what would happen"),
):
    # IMPORTANT: dry-run should NOT require DB connectivity
    if dry_run:
        console.print("[yellow]DRY RUN:[/yellow] would create student")
        console.print({"first_name": first_name, "last_name": last_name, "email": email})
        raise typer.Exit(code=0)

    s = load_settings()
    with get_conn(s) as conn:
        try:
            row = students_mod.create_student(conn, first_name, last_name, email)
            conn.commit()
        except ValueError as e:
            # e.g. duplicate email, validation, etc.
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(code=1)

    render_kv("Created", row)


@students.command("update")
def students_update(
    student_id: int = typer.Argument(..., help="Student ID"),
    first_name: str | None = typer.Option(None, "--first-name", help="New first name"),
    last_name: str | None = typer.Option(None, "--last-name", help="New last name"),
    email: str | None = typer.Option(None, "--email", help="New email"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Don't write; only show what would happen"),
):
    s = load_settings()
    with get_conn(s) as conn:
        before = students_mod.get_student(conn, student_id)
        if not before:
            console.print("[red]Not found.[/red]")
            raise typer.Exit(code=1)

        if dry_run:
            console.print("[yellow]DRY RUN:[/yellow] would update student")

            patch = {}
            if first_name is not None:
                patch["first_name"] = first_name
            if last_name is not None:
                patch["last_name"] = last_name
            if email is not None:
                patch["email"] = email

            if not patch:
                console.print("[yellow]No changes provided.[/yellow]")
                raise typer.Exit(code=0)

            console.print({"id": student_id, **patch})
            render_kv("Before", before)
            raise typer.Exit(code=0)

        try:
            after = students_mod.update_student(conn, student_id, first_name, last_name, email)
            conn.commit()
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(code=1)

    render_kv("Before", before)
    render_kv("After", after)


@students.command("delete")
def students_delete(
    student_id: int = typer.Argument(..., help="Student ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
):
    s = load_settings()
    with get_conn(s) as conn:
        row = students_mod.get_student(conn, student_id)
        if not row:
            console.print("[red]Not found.[/red]")
            raise typer.Exit(code=1)

        if not yes:
            ok = Confirm.ask(f"Delete student #{student_id} ({row.get('email')})?")
            if not ok:
                console.print("[yellow]Cancelled.[/yellow]")
                raise typer.Exit(code=0)

        deleted = students_mod.delete_student(conn, student_id)
        conn.commit()

    if deleted == 1:
        console.print("[green]Deleted.[/green]")
    else:
        console.print("[red]Delete failed.[/red]")
        raise typer.Exit(code=1)


# -----------------------
# Ops commands
# -----------------------

@ops.command("db-status")
def ops_db_status():
    s = load_settings()
    with get_conn(s) as conn:
        info = health_mod.db_status(conn)
    render_kv("DB Status", info)


@ops.command("permissions-check")
def ops_permissions_check():
    s = load_settings()
    with get_conn(s) as conn:
        info = health_mod.permissions_check(conn)

    render_kv("Permissions Check", info)

    # Expect schema_create = False for app_user
    if info and info.get("schema_create") is True:
        console.print("[red]WARNING:[/red] app_user can CREATE in schema public (not hardened).")
        raise typer.Exit(code=1)


@ops.command("seed-status")
def ops_seed_status():
    s = load_settings()
    with get_conn(s) as conn:
        info = health_mod.seed_status(conn)
    render_kv("Seed Status", info)


@ops.command("flyway-info")
def ops_flyway_info():
    s = load_settings()
    with get_conn(s) as conn:
        info = flyway_mod.flyway_info(conn)

    render_kv("Flyway Counts", info.get("counts"))
    render_kv("Flyway Latest", info.get("latest"))


@ops.command("flyway-recent")
def ops_flyway_recent(
    n: int = typer.Option(10, "--n", help="How many recent migrations to show")
):
    s = load_settings()
    with get_conn(s) as conn:
        rows = flyway_mod.flyway_recent(conn, n)
    render_table(rows, f"Flyway Recent (n={n})")


if __name__ == "__main__":
    app()
