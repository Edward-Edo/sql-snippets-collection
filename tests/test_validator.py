"""Tests para el validador de snippets."""

from __future__ import annotations

from pathlib import Path

import pytest

from devsql.validator import _first_statement, _strip_comments, discover_snippets, validate_snippet


def test_strip_comments() -> None:
    sql = "-- comentario\nSELECT 1; /* bloque */"
    cleaned = _strip_comments(sql)
    assert "comentario" not in cleaned
    assert "bloque" not in cleaned
    assert "SELECT 1" in cleaned


def test_first_statement() -> None:
    sql = "SELECT 1; SELECT 2;"
    assert _first_statement(sql).upper().startswith("SELECT 1")


def test_discover_snippets(tmp_path: Path) -> None:
    (tmp_path / "a.sql").write_text("SELECT 1;", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.sql").write_text("SELECT 2;", encoding="utf-8")
    (tmp_path / ".hidden").mkdir()
    (tmp_path / ".hidden" / "c.sql").write_text("SELECT 3;", encoding="utf-8")
    snippets = discover_snippets(tmp_path)
    assert len(snippets) == 2
    assert all("hidden" not in str(s) for s in snippets)


def test_validate_valid_sqlite(tmp_path: Path) -> None:
    snippet = tmp_path / "valid.sql"
    snippet.write_text("CREATE TABLE t (id INTEGER PRIMARY KEY);", encoding="utf-8")
    ok, msg = validate_snippet(snippet, dialect="sqlite")
    assert ok, msg


def test_validate_invalid_sqlite(tmp_path: Path) -> None:
    snippet = tmp_path / "invalid.sql"
    snippet.write_text("SELECT FROM WHERE;", encoding="utf-8")
    ok, _ = validate_snippet(snippet, dialect="sqlite")
    assert not ok


def test_validate_empty(tmp_path: Path) -> None:
    snippet = tmp_path / "empty.sql"
    snippet.write_text("", encoding="utf-8")
    ok, _ = validate_snippet(snippet, dialect="sqlite")
    assert not ok


def test_real_collection_validates() -> None:
    """Asegura que todos los snippets reales del repo son válidos contra SQLite."""
    from devsql.validator import discover_snippets

    root = Path(__file__).resolve().parent.parent / "snippets"
    if not root.exists():
        pytest.skip("Directorio snippets/ no presente en este entorno.")
    failures = []
    for s in discover_snippets(root):
        ok, msg = validate_snippet(s, dialect="sqlite")
        if not ok:
            failures.append((s, msg))
    assert not failures, f"Snippets inválidos: {failures}"
