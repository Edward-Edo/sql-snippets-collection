# 🗄️ sql-snippets-collection

[![CI](https://github.com/Edward-Edo/sql-snippets-collection/actions/workflows/ci.yml/badge.svg)](https://github.com/Edward-Edo/sql-snippets-collection/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Snippets](https://img.shields.io/badge/snippets-15+-orange)]()

Colección **curada y validada** de snippets SQL para MySQL, PostgreSQL y migraciones Laravel.
Cada snippet incluye comentarios con título, dialecto y descripción, y se valida automáticamente contra **SQLite en memoria** con un validador CLI propio.

---

## 📚 Contenido

| Categoría       | Snippets | Temas cubiertos                                                                 |
|-----------------|---------:|---------------------------------------------------------------------------------|
| `mysql/`        | 5        | Top N por grupo, upsert, búsqueda full-text, series recursivas, duplicados.      |
| `postgresql/`   | 5        | `ROW_NUMBER`, ventanas, CTE recursivo, upsert, `crosstab`, keyset pagination.   |
| `laravel/`      | 4        | Polimórfica tags, posts con índices, soft deletes, auditoría con JSON.          |
| **Total**       | **14**   |                                                                                 |

> Lista completa: [`snippets/`](snippets/).

---

## 🚀 Uso

### Navega y copia

Cada archivo `.sql` es autocontenido. Cópialo y pégalo en tu editor o cliente SQL favorito.

### Validador CLI

Incluye una herramienta (`devsql`) para validar y auditar la colección localmente.

```bash
# Instalar en modo editable
git clone https://github.com/Edward-Edo/sql-snippets-collection.git
cd sql-snippets-collection
pip install -e ".[dev]"

# Validar todos los snippets contra SQLite en memoria
devsql validate snippets/

# Listar con metadata
devsql list snippets/

# Estadísticas globales
devsql stats snippets/
# {
#   "total_snippets": 14,
#   "total_lines": 220,
#   "by_dialect": {"postgresql": 5, "mysql": 5, "laravel": 4}
# }
```

---

## 🧪 Tests

```bash
pip install -e ".[dev]"
pytest
ruff check tools tests
```

La suite valida que:

1. El parser de comentarios funciona correctamente.
2. El descubridor de archivos respeta `.gitignore` y excluye directorios ocultos.
3. **Todos los snippets reales** se ejecutan sin error en SQLite.

---

## 📐 Convención de nombres

```
<dialecto>_<slug_descriptivo>.sql
```

Cada archivo empieza con un encabezado de tres comentarios:

```sql
-- Title: ...
-- Dialect: mysql | postgresql | laravel | sqlite | any
-- Description: ...
```

---

## 🤝 Contribuir

¿Tienes un snippet útil y probado? Sigue estos pasos:

1. Fork & branch: `git checkout -b feat/snippet-mi-caso`
2. Crea el archivo siguiendo la **convención de nombres** y el encabezado.
3. Ejecuta `devsql validate snippets/` — debe pasar.
4. Abre un Pull Request con una breve justificación.

Reglas:
- Snippets probados en su dialecto real cuando sea posible.
- Comentarios claros en la cabecera.
- Sin dependencias de datos específicos del autor.

---

## 📄 Licencia

[MIT](LICENSE) © 2026 Edward Itriago

---

## ✍️ Autor

**Edward Itriago** — Full Stack Developer
📧 edwarditriagosub@gmail.com · 🔗 [github.com/Edward-Edo](https://github.com/Edward-Edo)
