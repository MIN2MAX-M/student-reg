from rich.table import Table
from rich.console import Console

console = Console()


def render_table(rows: list[dict], title: str):
    table = Table(title=title, show_lines=False)
    if not rows:
        console.print("[yellow]No results.[/yellow]")
        return

    for col in rows[0].keys():
        table.add_column(str(col))

    for r in rows:
        table.add_row(*[str(r.get(c, "")) for c in rows[0].keys()])

    console.print(table)


def render_kv(title: str, d: dict | None):
    console.print(f"[bold]{title}[/bold]")
    if not d:
        console.print("[yellow]None[/yellow]")
        return
    for k, v in d.items():
        console.print(f"  [cyan]{k}[/cyan]: {v}")
