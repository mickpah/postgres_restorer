disconnect_drop_and_setup_db = \
    '''
    CREATE OR REPLACE FUNCTION pg_temp.set_up_db(test_db_name TEXT, conn_string TEXT)
    RETURNS VOID AS $$
    BEGIN
        PERFORM pg_terminate_backend (pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = test_db_name;
    
        CREATE EXTENSION IF NOT EXISTS dblink;
    
        PERFORM dblink_connect(conn_string);
        PERFORM dblink_exec('DROP DATABASE IF EXISTS ' || test_db_name);
        PERFORM dblink_exec('CREATE DATABASE ' || test_db_name);
    END
    $$
    LANGUAGE plpgsql;
    
    SELECT pg_temp.set_up_db(%(test_db_name)s, %(conn_string)s);
    '''

tear_down_db = \
    '''
    CREATE OR REPLACE FUNCTION pg_temp.tear_down_db(test_db_name TEXT, conn_string TEXT)
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
    
    SELECT pg_temp.tear_down_db(%(test_db_name)s, %(conn_string)s);
    '''