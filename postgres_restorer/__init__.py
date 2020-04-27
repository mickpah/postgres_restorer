import os
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

    def fetch(self, query: str, params: dict, first: bool = False):
        try:
            self._open_connection(self._test_db_name)
            self._cursor.execute(query, params)

            if first:
                return dict(self._cursor.fetchone())

            return dict(self._cursor.fetchall())
        except Error as error:
            raise PostgresRestorerError(f'Error during executing query:\n{query}!', error.__dict__)
        finally:
            self._close_connection()

    def execute(self, query: str, params: dict = None):
        try:
            self._open_connection(self._test_db_name)
            self._cursor.execute(query, params)
        except Error as error:
            raise PostgresRestorerError(f'Error during executing query:\n{query}!', error.__dict__)
        finally:
            self._close_connection()

    def commit(self):
        try:
            self._connection.commit()
            self._close_connection()
        except Error as error:
            raise PostgresRestorerError(f'Commit failed!', error.__dict__)

    def rollback(self):
        try:
            self._connection.rollback()
            self._close_connection()
        except Error as error:
            raise PostgresRestorerError(f'Rollback failed!', error.__dict__)

    def setup(self):
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
