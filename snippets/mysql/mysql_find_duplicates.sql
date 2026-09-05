-- Title: Encontrar filas duplicadas
-- Dialect: mysql
-- Description: Lista de emails duplicados junto con el conteo de ocurrencias.

SELECT email, COUNT(*) AS occurrences
FROM users
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;
