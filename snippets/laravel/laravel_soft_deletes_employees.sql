-- Title: Soft deletes + columna computed de antigüedad
-- Dialect: laravel
-- Description: Tabla de empleados con soft deletes y columna generada para años de servicio.

CREATE TABLE employees (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    hired_at DATE NOT NULL,
    terminated_at DATE NULL,
    deleted_at TIMESTAMP NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL,
    years_of_service INT GENERATED ALWAYS AS (
        IFNULL(TIMESTAMPDIFF(YEAR, hired_at, COALESCE(terminated_at, CURDATE())), 0)
    ) STORED,
    INDEX idx_hired (hired_at),
    INDEX idx_deleted (deleted_at)
);
