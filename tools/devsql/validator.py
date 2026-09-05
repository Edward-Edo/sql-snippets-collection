"""Validación y descubrimiento de snippets SQL."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

_SQL_COMMENT = re.compile(r"--[^\n]*")
_SQL_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)


def discover_snippets(root: Path) -> list[Path]:
    """Descubre archivos .sql en `root` recursivamente, excluyendo directorios ocultos."""
    return sorted(p for p in root.rglob("*.sql") if not any(part.startswith(".") for part in p.parts))


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


def validate_snippet(path: Path, dialect: str = "any") -> tuple[bool, str]:
    """Valida un snippet. dialect in {mysql, postgresql, sqlite, any}.

    - Si `dialect=any` se ejecuta contra SQLite en memoria.
    - Si `dialect=mysql|postgresql`, se valida por heurística de marcadores comunes.
    """
    try:
        sql = path.read_text(encoding="utf-8")
    except OSError as exc:
        return False, f"Error de lectura: {exc}"

    if not sql.strip():
        return False, "Snippet vacío."

    if dialect == "any" or dialect == "sqlite":
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

    if dialect == "mysql":
        if re.search(r"\b(MONEY|INTERVAL\s+'|::\w+|RETURNING)\b", sql, re.IGNORECASE):
            return False, "Marcador PostgreSQL detectado en snippet MySQL."
        return True, "OK (heurística MySQL)"

    if dialect == "postgresql":
        if re.search(r"\bENGINE\s*=\s*InnoDB\b", sql, re.IGNORECASE):
            return False, "Marcador MySQL detectado en snippet PostgreSQL."
        return True, "OK (heurística PostgreSQL)"

    return False, f"Dialect no soportado: {dialect}"
