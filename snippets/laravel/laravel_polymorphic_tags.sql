-- Title: Tabla de tags polimórfica
-- Dialect: laravel
-- Description: Esquema polimórfico muchos-a-muchos (taggables).

CREATE TABLE tags (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL
);

CREATE TABLE taggables (
    tag_id BIGINT UNSIGNED NOT NULL,
    taggable_id BIGINT UNSIGNED NOT NULL,
    taggable_type VARCHAR(255) NOT NULL,
    PRIMARY KEY (tag_id, taggable_id, taggable_type),
    INDEX idx_taggable (taggable_type, taggable_id)
);
