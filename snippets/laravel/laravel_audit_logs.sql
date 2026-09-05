-- Title: Auditoría mínima con JSON y trigger (MySQL 8+)
-- Dialect: laravel
-- Description: Registra cambios en una columna JSON vía trigger BEFORE UPDATE.

CREATE TABLE audit_logs (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    auditable_type VARCHAR(100) NOT NULL,
    auditable_id BIGINT UNSIGNED NOT NULL,
    event VARCHAR(20) NOT NULL,
    old_values JSON NULL,
    new_values JSON NULL,
    user_id BIGINT UNSIGNED NULL,
    created_at TIMESTAMP NULL,
    INDEX idx_auditable (auditable_type, auditable_id)
);
