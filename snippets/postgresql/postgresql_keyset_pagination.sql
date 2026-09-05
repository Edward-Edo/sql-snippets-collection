-- Title: Paginación eficiente con keyset (seek)
-- Dialect: postgresql
-- Description: Paginación estable y rápida para grandes volúmenes de datos.

SELECT id, title, created_at
FROM articles
WHERE (created_at, id) < ($1, $2)
ORDER BY created_at DESC, id DESC
LIMIT 20;
