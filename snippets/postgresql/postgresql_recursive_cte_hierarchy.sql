-- Title: CTE recursivo para jerarquía de categorías
-- Dialect: postgresql
-- Description: Devuelve el árbol completo de categorías hijas a partir de una raíz.

WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 1 AS depth
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id, t.depth + 1
    FROM categories c
    INNER JOIN category_tree t ON c.parent_id = t.id
)
SELECT id, name, parent_id, depth FROM category_tree;
