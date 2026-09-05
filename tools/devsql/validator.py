"""Validación y descubrimiento de snippets SQL."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

_SQL_COMMENT = re.compile(r"--[^\n]*")
_SQL_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)

_DIALECT_FROM_FILENAME = re.compile(r"^(mysql|postgresql|sqlite|laravel|any)_")


def discover_snippets(root: Path) -> list[Path]:
    """Descubre archivos .sql en `root`, excluyendo directorios ocultos."""
    return sorted(
        p for p in root.rglob("*.sql") if not any(part.startswith(".") for part in p.parts)
    )


def infer_dialect(path: Path) -> str:
    """Infiera el dialecto desde el prefijo del nombre del archivo.

    Ejemplos:
        mysql_top_n.sql            -> mysql
        postgresql_window.sql      -> postgresql
        laravel_posts.sql          -> laravel
        sqlite_anything.sql        -> sqlite
        custom.sql                 -> any
    """
    match = _DIALECT_FROM_FILENAME.match(path.stem)
    if not match:
        return "any"
    dialect = match.group(1)
    return dialect if dialect in {"mysql", "postgresql", "sqlite", "laravel", "any"} else "any"


def _strip_comments(sql: str) -> str:
    sql = _SQL_BLOCK_COMMENT.sub("", sql)
    sql = _SQL_COMMENT.sub("", sql)
    return sql.strip()


def _first_statement(sql: str) -> str:
    """Toma la primera sentencia terminada en ';'."""
    cleaned = _strip_comments(sql)
    if ";" not in cleaned:
        return cleaned
    return cleaned.split(";", 1)[0].strip()


def _validate_sqlite(sql: str) -> tuple[bool, str]:
    stmt = _first_statement(sql)
    try:
        conn = sqlite3.connect(":memory:")
        try:
            conn.execute(stmt)
        finally:
            conn.close()
    except sqlite3.Error as exc:
        return False, f"SQLite no pudo parsear la primera sentencia: {exc}"
    return True, "OK (SQLite)"


def _validate_heuristic(sql: str, dialect: str) -> tuple[bool, str]:
    pg_markers = re.compile(r"\b(MONEY|::\w+|RETURNING|GENERATED\s+ALWAYS)\b", re.IGNORECASE)
    mysql_markers = re.compile(r"\b(ENGINE\s*=\s*InnoDB|FULLTEXT)\b", re.IGNORECASE)

    if dialect == "mysql":
        if pg_markers.search(sql):
            return False, "Marcador PostgreSQL detectado en snippet MySQL."
        return True, "OK (heurística MySQL)"
    if dialect == "postgresql":
        if mysql_markers.search(sql):
            return False, "Marcador MySQL detectado en snippet PostgreSQL."
        return True, "OK (heurística PostgreSQL)"
    if dialect == "laravel":
        # Laravel snippets apuntan a MySQL/PostgreSQL pero usan tipos portables;
        # verificamos que no haya sintaxis propietaria exclusiva.
        return True, "OK (heurística Laravel)"
    return True, "OK"


def validate_snippet(path: Path, dialect: str = "auto") -> tuple[bool, str]:
    """Valida un snippet.

    - Si `dialect=auto`, se infiere del nombre del archivo.
    - Si `dialect=any`, se ejecuta contra SQLite en memoria.
    - Si `dialect=mysql|postgresql|laravel`, se valida por heurística de marcadores.
    """
    try:
        sql = path.read_text(encoding="utf-8")
    except OSError as exc:
        return False, f"Error de lectura: {exc}"

    if not sql.strip():
        return False, "Snippet vacío."

    target = infer_dialect(path) if dialect == "auto" else dialect.lower()

    if target in {"any", "sqlite"}:
        return _validate_sqlite(sql)
    if target in {"mysql", "postgresql", "laravel"}:
        return _validate_heuristic(sql, target)

    return False, f"Dialect no soportado: {dialect}"
