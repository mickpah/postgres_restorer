check_if_database_exists = \
    '''
    SELECT EXISTS (SELECT FROM pg_database WHERE datname=%(dbname)s);
    '''

drop_test_db = \
    '''
    CREATE OR REPLACE FUNCTION pg_temp.drop_db(test_db_name TEXT, conn_string TEXT)
    RETURNS VOID AS $$
    BEGIN
        PERFORM pg_terminate_backend (pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = test_db_name;
    
        CREATE EXTENSION IF NOT EXISTS dblink;
    
        PERFORM dblink_connect(conn_string);
        PERFORM dblink_exec('DROP DATABASE IF EXISTS ' || test_db_name);
    END
    $$
        LANGUAGE plpgsql;
    
    SELECT pg_temp.drop_db(%(test_db_name)s, %(conn_string)s);
    '''

check_if_table_exist = \
    '''
    SELECT EXISTS(
        SELECT FROM pg_catalog.pg_class
        JOIN pg_catalog.pg_namespace ON pg_catalog.pg_namespace.OID = pg_catalog.pg_class.relnamespace
        WHERE pg_catalog.pg_namespace.nspname = %(schema_name)s
        AND pg_catalog.pg_class.relname = %(table_name)s
        AND pg_catalog.pg_class.relkind = 'r'
    );
    '''

check_if_data_inserted_table_1 = \
    '''
    SELECT name FROM test_table_1;
    '''

check_if_data_inserted_table_2 = \
    '''
    SELECT name FROM test_table_2;
    '''

check_if_data_inserted_table_3 = \
    '''
    SELECT name FROM test_table_3;
    '''

execute_test_insert = \
    '''
    INSERT INTO test_table_1(name)
    VALUES ('inserted_test_name_1');
    '''

test_execute_insert_result = \
    '''
        SELECT name FROM test_table_1
        WHERE name='inserted_test_name_1';
    '''

test_fetch_result = \
    '''
    SELECT name FROM test_table_1
    ORDER BY name;
    '''
