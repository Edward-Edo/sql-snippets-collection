-- Title: Suma acumulada con ventana
-- Dialect: postgresql
-- Description: Calcula suma móvil (running total) por usuario ordenado por fecha.

SELECT
    user_id,
    created_at,
    amount,
    SUM(amount) OVER (
        PARTITION BY user_id
        ORDER BY created_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM transactions;
