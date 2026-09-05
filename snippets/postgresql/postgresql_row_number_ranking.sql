-- Title: Ranking de usuarios con ROW_NUMBER
-- Dialect: postgresql
-- Description: Obtiene el top N de usuarios por score, numerando empates de forma estable.

SELECT
    id,
    name,
    score,
    ROW_NUMBER() OVER (
        PARTITION BY category_id
        ORDER BY score DESC, created_at ASC
    ) AS rank
FROM users
WHERE score > 0
ORDER BY category_id, rank;
