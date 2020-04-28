import pytest
from psycopg2 import connect

from postgres_restorer import PostgresRestorer
from tests.test_queries import check_if_database_exists, drop_test_db, check_if_table_exist, \
    check_if_data_inserted_table_1, check_if_data_inserted_table_2, check_if_data_inserted_table_3, execute_test_insert, \
    test_execute_insert_result, test_fetch_result

config = {
    'server_connection_string': 'host=localhost user=postgres password=postgres ',
    'test_db_name': 'test_database',
    'dbup_scripts_path': './dbup_scripts',
    'test_data_scripts_path': './test_data_scripts'
}


@pytest.fixture(autouse=True)
def restorer() -> PostgresRestorer:
    return PostgresRestorer(
        server_connection_string=config['server_connection_string'],
        test_db_name=config['test_db_name'],
        dbup_scripts_path=config['dbup_scripts_path'],
        test_data_scripts_path=config['test_data_scripts_path']
    )


def _check_if_table_exists(conn, table_name: str, schema_name: str):
    with conn.cursor() as cursor:
        cursor.execute(
            check_if_table_exist,
            {
                'table_name': table_name,
                'schema_name': schema_name
            })
        return cursor.fetchone()[0]


def _check_if_data_exists(conn, query: str, expected_data: list):
    with conn.cursor() as cursor:
        cursor.execute(
            query)
        fetched_data = cursor.fetchall()
        results = [result[0] for result in fetched_data] if \
            isinstance(fetched_data, list) else \
            fetched_data[0]
        return all(data in expected_data for data in results)


def _connect(dbname: str):
    connection_string = \
        f"{config['server_connection_string']} " + \
        f"dbname={dbname}"

    connection = connect(connection_string)
    connection.autocommit = True
    return connection


class Test_SetupOnce_WorksCorrectly_DatabaseCreated:
    def test_setup_once(self, restorer: PostgresRestorer):
        # setup
        conn = _connect('postgres')

        with conn.cursor() as cursor:
            cursor.execute(drop_test_db,
                           {
                               'test_db_name': config['test_db_name'],
                               'conn_string': f"{config['server_connection_string']} " + \
                                              f"dbname=postgres"
                           })

        # test
        restorer.setup_once()

        # assertion
        with conn.cursor() as cursor:
            cursor.execute(check_if_database_exists, {'dbname': config['test_db_name']})
            result = cursor.fetchone()

        assert result[0]

        # cleanup
        conn.close()


class Test_TearDownOnce_WorksCorrectly_DatabaseDropped:
    def test_teardown_once(self, restorer: PostgresRestorer):
        # setup
        restorer.setup_once()

        conn = _connect('postgres')

        with conn.cursor() as cursor:
            cursor.execute(check_if_database_exists, {'dbname': config['test_db_name']})
            does_database_exists = cursor.fetchone()

        assert does_database_exists

        # test
        restorer.teardown_once()

        # assertion
        with conn.cursor() as cursor:
            cursor.execute(check_if_database_exists, {'dbname': config['test_db_name']})
            result = cursor.fetchone()

        assert not result[0]

        # cleanup
        conn.close()


class Test_Setup_WorksCorrectly_SchemaCreatedAndFilledWithTestData:
    def test_setup(self, restorer: PostgresRestorer):
        # setup
        restorer.setup_once()

        conn = _connect('postgres')

        with conn.cursor() as cursor:
            cursor.execute(check_if_database_exists, {'dbname': config['test_db_name']})
            does_database_exists = cursor.fetchone()[0]

        assert does_database_exists

        conn.close()
        expected_data = ['test1', 'test2']

        # test
        restorer.setup()

        # assertion
        conn = _connect(config['test_db_name'])

        assert _check_if_table_exists(conn, 'test_table_1', 'public')
        assert _check_if_table_exists(conn, 'test_table_2', 'public')
        assert _check_if_table_exists(conn, 'test_table_3', 'public')
        assert _check_if_data_exists(conn, check_if_data_inserted_table_1, expected_data)
        assert _check_if_data_exists(conn, check_if_data_inserted_table_2, expected_data)
        assert _check_if_data_exists(conn, check_if_data_inserted_table_3, expected_data)

        # cleanup
        conn.close()


class Test_Execute_WorksCorrectly_ExecutesQuery:
    def test_execute(self, restorer: PostgresRestorer):
        # setup
        restorer.setup_once()
        restorer.setup()
        expected_results = ['inserted_test_name_1']
        conn = _connect(config['test_db_name'])

        # test
        restorer.execute(execute_test_insert)

        # assertion
        assert _check_if_data_exists(conn, test_execute_insert_result, expected_results)

        # cleanup
        conn.close()


class Test_Fetch_WorksCorrectlyFirstTrue_ReturnsFirstQueryResult:
    def test_fetch(self, restorer: PostgresRestorer):
        # setup
        restorer.setup_once()
        restorer.setup()
        expected_result = 'test1'
        conn = _connect(config['test_db_name'])

        # test
        result = restorer.fetch(query=test_fetch_result, first=True)

        # assertion
        assert result['name'] == expected_result


class Test_Fetch_WorksCorrectlyFirstFalse_ReturnsListOfResults:
    def test_fetch(self, restorer: PostgresRestorer):
        # setup
        restorer.setup_once()
        restorer.setup()
        expected_result = ['test1', 'test2']
        conn = _connect(config['test_db_name'])

        # test
        results = restorer.fetch(query=test_fetch_result, first=False)
        results = [result['name'] for result in results]

        assert all(data in expected_result for data in results)
