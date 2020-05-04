CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE TestTable(
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
)