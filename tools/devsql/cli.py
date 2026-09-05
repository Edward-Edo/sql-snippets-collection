"""CLI de devsql: validar y listar snippets SQL."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from .validator import discover_snippets, validate_snippet

console = Console(stderr=True)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(package_name="sql-snippets-collection", prog_name="devsql")
def main() -> None:
    """🗄️ devsql — herramientas para la colección de snippets SQL."""


@main.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--dialect",
    type=click.Choice(["auto", "mysql", "postgresql", "sqlite", "laravel", "any"], case_sensitive=False),
    default="auto",
    show_default=True,
    help="Dialect para validación. 'auto' infiere del nombre del archivo.",
)
@click.option("--fail-fast", is_flag=True, help="Detener al primer error.")
def validate(path: Path, dialect: str, fail_fast: bool) -> None:
    """Valida sintaxis básica de todos los snippets en PATH."""
    snippets = discover_snippets(path)
    if not snippets:
        click.echo(f"[WARN] No se encontraron snippets en {path}", err=True)
        sys.exit(0)

    errors = 0
    for snippet in snippets:
        ok, msg = validate_snippet(snippet, dialect=dialect.lower())
        marker = "[green]✓[/]" if ok else "[red]✗[/]"
        line = f"{marker} {snippet.relative_to(path)} — {msg}"
        if ok:
            click.echo(line)
        else:
            console.print(line)
            errors += 1
            if fail_fast:
                sys.exit(1)

    if errors:
        console.print(f"\n[red]✗ {errors} snippet(s) con errores.[/]")
        sys.exit(1)
    console.print(f"\n[green]✓ {len(snippets)} snippet(s) válidos.[/]")


@main.command(name="list")
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
def list_cmd(path: Path) -> None:
    """Lista todos los snippets y muestra su metadata."""
    snippets = discover_snippets(path)
    table = Table(title=f"Snippets en {path}", show_header=True, header_style="bold magenta")
    table.add_column("Archivo", style="cyan", no_wrap=True)
    table.add_column("Dialect", style="white")
    table.add_column("Líneas", justify="right", style="green")
    for s in snippets:
        meta = s.stem.split("_", 1)[0]
        lines = sum(1 for _ in s.open(encoding="utf-8"))
        table.add_row(str(s.relative_to(path)), meta, str(lines))
    console.print(table)


@main.command(name="stats")
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
def stats_cmd(path: Path) -> None:
    """Muestra estadísticas globales de la colección."""
    snippets = discover_snippets(path)
    by_dialect: dict[str, int] = {}
    total_lines = 0
    for s in snippets:
        dialect = s.stem.split("_", 1)[0]
        by_dialect[dialect] = by_dialect.get(dialect, 0) + 1
        total_lines += sum(1 for _ in s.open(encoding="utf-8"))
    payload = {
        "total_snippets": len(snippets),
        "total_lines": total_lines,
        "by_dialect": by_dialect,
    }
    click.echo(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
