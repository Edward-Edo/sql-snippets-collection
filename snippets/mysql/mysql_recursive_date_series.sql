-- Title: Generar serie de fechas
-- Dialect: mysql
-- Description: Genera un calendario de los últimos 30 días usando una CTE recursiva (MySQL 8+).

WITH RECURSIVE calendar(d) AS (
    SELECT CURDATE() - INTERVAL 29 DAY
    UNION ALL
    SELECT d + INTERVAL 1 DAY FROM calendar WHERE d < CURDATE()
)
SELECT d AS day FROM calendar;
