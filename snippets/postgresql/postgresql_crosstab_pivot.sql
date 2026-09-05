-- Title: Pivot dinámico con crosstab
-- Dialect: postgresql
-- Description: Convierte filas por mes en columnas, una por cada mes del año.

SELECT * FROM crosstab(
    $$ SELECT user_id, DATE_TRUNC('month', created_at), COUNT(*)
        FROM events
        WHERE created_at >= NOW() - INTERVAL '12 months'
        GROUP BY 1, 2
        ORDER BY 1, 2 $$,
    $$ SELECT generate_series(
            DATE_TRUNC('year', NOW()),
            DATE_TRUNC('year', NOW()) + INTERVAL '11 months',
            INTERVAL '1 month'
       ) $$
) AS ct(user_id BIGINT, m01 BIGINT, m02 BIGINT, m03 BIGINT, m04 BIGINT,
        m05 BIGINT, m06 BIGINT, m07 BIGINT, m08 BIGINT, m09 BIGINT,
        m10 BIGINT, m11 BIGINT, m12 BIGINT);
