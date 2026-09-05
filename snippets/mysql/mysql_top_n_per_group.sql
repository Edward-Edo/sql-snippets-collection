-- Title: Top N por grupo
-- Dialect: mysql
-- Description: Devuelve los 3 productos más vendidos por categoría usando variables de sesión.

SELECT category_id, product_id, total_sold
FROM (
    SELECT
        category_id,
        product_id,
        total_sold,
        @row_number := IF(@prev_cat = category_id, @row_number + 1, 1) AS rn,
        @prev_cat := category_id
    FROM (
        SELECT category_id, product_id, SUM(quantity) AS total_sold
        FROM sales
        GROUP BY category_id, product_id
        ORDER BY category_id, total_sold DESC
    ) AS ranked,
    (SELECT @row_number := 0, @prev_cat := NULL) AS vars
) AS numbered
WHERE rn <= 3
ORDER BY category_id, rn;
