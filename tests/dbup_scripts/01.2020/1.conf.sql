DROP SCHEMA IF EXISTS public;
CREATE SCHEMA public;

CREATE TABLE test_table_1(
    id SERIAL PRIMARY KEY,
    name TEXT
);