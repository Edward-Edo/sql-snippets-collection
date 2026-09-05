-- Title: Búsqueda full-text con MATCH ... AGAINST
-- Dialect: mysql
-- Description: Índice FULLTEXT para búsqueda por relevancia en InnoDB (MySQL 5.6+).

SELECT id, title, MATCH(title, body) AGAINST('laravel livewire' IN NATURAL LANGUAGE MODE) AS relevance
FROM articles
WHERE MATCH(title, body) AGAINST('laravel livewire' IN NATURAL LANGUAGE MODE)
ORDER BY relevance DESC
LIMIT 20;
