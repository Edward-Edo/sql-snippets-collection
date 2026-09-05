-- Title: Upsert con ON DUPLICATE KEY UPDATE
-- Dialect: mysql
-- Description: Inserta o actualiza el stock de un producto por su SKU.

INSERT INTO inventory (sku, qty, updated_at)
VALUES ('ABC-001', 10, NOW())
ON DUPLICATE KEY UPDATE
    qty = VALUES(qty),
    updated_at = VALUES(updated_at);
