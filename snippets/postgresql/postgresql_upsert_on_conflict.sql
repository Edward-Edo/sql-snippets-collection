-- Title: Upsert con ON CONFLICT
-- Dialect: postgresql
-- Description: Inserta un usuario o actualiza su email si el username ya existe.

INSERT INTO users (username, email, created_at)
VALUES ('edward', 'edward@example.com', NOW())
ON CONFLICT (username) DO UPDATE
SET email = EXCLUDED.email,
    updated_at = NOW();
