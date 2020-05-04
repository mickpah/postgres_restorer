from contextlib import contextmanager
from typing import Dict
from .pg_connection import PG_Connection


class Connector:
    def __init__(self, settings: Dict, current_db: str):
        self._settings = settings
        self.current_db = current_db

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value

    @property
    def connection_string(self):
        conn_info = self.settings['connection_info']
        return f"host='{conn_info['host']}' user='{conn_info['user']}' " \
               f"password='{conn_info['password']}' dbname='{self.current_db}'"

    @property
    def restore_db(self):
        return self.settings['test_db_name']

    @property
    def path_to_restore(self):
        return self.settings['restore_path']

    @property
    def env_vars(self):
        conn_info = self.settings['connection_info']
        return {
            'PGPASSWORD': conn_info['password'],
            'PGHOST': conn_info['host'],
            'PGUSER': conn_info['user']
        }

    @property
    def cursor_type(self):
        return self.settings['cursor_type']

    @property
    def autocommit(self):
        return self.settings['autocommit']

    @property
    @contextmanager
    def cursor(self):
        with PG_Connection(
                self.connection_string, self.cursor_type, self.autocommit
        ) as connection:
            with connection.cursor() as _cursor:
                yield _cursor
