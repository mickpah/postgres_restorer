import os
from typing import Union, List, Dict

from psycopg2 import connect, Error
from psycopg2.extras import DictCursor
from postgres_restorer._errors import PostgresRestorerError
from postgres_restorer._queries import disconnect_drop_and_setup_db, tear_down_db


class PostgresRestorer:
    def __init__(
            self,
            server_connection_string: str,
            test_db_name: str,
            dbup_scripts_path: str,
            test_data_scripts_path: str
    ):
        """
        PostgresRestorer enables:
            - Creating/dropping test database.
            - Building appropriate schema.
            - Filling schema with test data.
            - Querying test database.

        Interface methods:
            - setup_once -> database creation
            - teardown_once -> database dropping
            - setup -> schema building/resetting,
              filling tables with test data
            - execute -> execute query on test database
            - fetch -> fetch data from test database

        :param server_connection_string: Connection string to postgres server
            without database name (restorer assumes that default 'postgres' database exists).
            Example: 'host=localhost user=test password=test'.

        :param test_db_name: Restorer will create test database with this value as its name.

        :param dbup_scripts_path: Path to folder with schema building scripts. Restorer expects
            following directory structure: dbup_scripts_folder/subfolder/script, where
            dbup_scripts_folder is location pointed by dbup_scripts_path, subfolders may mean
            month/year or sprint/year for example, as long as they are easily sortable chronologically,
            and scripts are schema building scripts (without database creation logic).

        :param test_data_scripts_path: Path to folder containing table-filling scripts with test data.
            Unlike 'dbup_scripts_path', 'test_data_scripts_path' has no subfolders, script files
            are placed directly in location pointed by this parameter.
        """
        self._server_connection_string = server_connection_string
        self._test_db_name = test_db_name
        self._connection = None
        self._cursor = None
        self._dbup_scripts_path = dbup_scripts_path
        self._test_data_scripts_path = test_data_scripts_path
        self._schema_script = None
        self._test_script = None

    def _build_schema_query(self) -> str:
        if self._schema_script:
            return self._schema_script

        folders = sorted(os.listdir(self._dbup_scripts_path))
        subscripts = []

        for folder in folders:
            scripts = sorted(
                os.listdir(
                    os.path.join(self._dbup_scripts_path, folder))
            )
            for script in scripts:
                file_path = os.path.join(self._dbup_scripts_path, folder, script)

                with open(file_path, 'r') as file:
                    subscripts.append(file.read())

        self._schema_script = ''.join(subscripts)

    def _build_test_query(self) -> str:
        if self._test_script:
            return self._test_script
        subscripts = []
        scripts = sorted(os.listdir(self._test_data_scripts_path))

        for script in scripts:
            file_path = os.path.join(self._test_data_scripts_path, script)
            with open(file_path, 'r') as file:
                subscripts.append(file.read())
        self._test_script = ''.join(subscripts)

    def _close_connection(self):
        try:
            if self._cursor:
                self._cursor.close()
            if self._connection:
                self._connection.close()
        except Error as error:
            raise PostgresRestorerError(f'Closing connection failed!', error.__dict__)

    def _open_connection(self, database_name):
        try:
            self._close_connection()
            self._connection = connect(f'{self._server_connection_string} dbname={database_name}',
                                       cursor_factory=DictCursor)
            self._connection.autocommit = True
            self._cursor = self._connection.cursor()
        except Error as error:
            raise PostgresRestorerError(f'Opening connection failed!', error.__dict__)

    def fetch(self, query: str, params: dict = None, first: bool = False) -> Union[Dict, List[Dict]]:
        """
        Fetch data from currently tested database.
        :param query: 'SELECT' query
        :param params: values for query parametrization passed as dictionary.
        :param first: If true only first result will be fetched.
            All results fetched by default.
        :return: Dictionary or list of dictionaries containing query result.
        :raises PostgresRestorerError:
        """
        try:
            self._open_connection(self._test_db_name)
            self._cursor.execute(query, params)

            if first:
                return dict(self._cursor.fetchone())

            return [dict(row) for row in self._cursor.fetchall()]
        except Error as error:
            raise PostgresRestorerError(f'Error during executing query:\n{query}!', error.__dict__)
        finally:
            self._close_connection()

    def execute(self, query: str, params: dict = None):
        """
        Execute query on currently tested database,
        without returning any values.
        :param query: 'SELECT' query
        :param params: values for query parametrization passed as dictionary.
        """
        try:
            self._open_connection(self._test_db_name)
            self._cursor.execute(query, params)
        except Error as error:
            raise PostgresRestorerError(f'Error during executing query:\n{query}!', error.__dict__)
        finally:
            self._close_connection()

    def setup(self):
        """
        Method that creates schemas in test database and fills them with data.
        First dbup script must have logic that drops and recreates all schemas
        used in database.
        Example:
        'DROP SCHEMA IF EXISTS public CASCADE;
        CREATE SCHEMA public;'
        This method should be called before each test.
        """
        try:
            self._build_schema_query()
            self.execute(self._schema_script)
            self._build_test_query()
            self.execute(self._test_script)
        except Error as error:
            raise PostgresRestorerError(f'Setting up schema failed!', error.__dict__)
        finally:
            self._close_connection()

    def setup_once(self):
        """
        Method that creates test database.
        If test database already exists it will be dropped and recreated.
        This method should be called once, before running tests.
        """
        try:
            self._open_connection('postgres')
            self._cursor.execute(
                disconnect_drop_and_setup_db,
                {
                    'test_db_name': self._test_db_name,
                    'conn_string': f'{self._server_connection_string} dbname=postgres'
                }
            )
        except Error as error:
            raise PostgresRestorerError(f'Setting up database failed!', error.__dict__)
        finally:
            self._close_connection()

    def teardown_once(self):
        """
        Method that drops test database.
        This method should be called once, after all tests finished.
        """
        try:
            self._open_connection('postgres')
            self._cursor.execute(
                tear_down_db,
                {
                    'test_db_name': self._test_db_name,
                    'conn_string': f'{self._server_connection_string} dbname=postgres'
                }
            )
        except Error as error:
            raise PostgresRestorerError(f'Tearing down database failed!', error.__dict__)
        finally:
            self._close_connection()
