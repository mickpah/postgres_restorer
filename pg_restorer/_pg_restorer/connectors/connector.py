from typing import Dict
from .pg_connection import PG_Connection


class Connector:
    def __init__(self, settings: Dict):
        self._settings = settings

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value

    @property
    def connection_string(self):
        return f"{self.settings['server_connection_string']} " \
               f"dbname={self.settings['test_db_name']}"

    @property
    def cursor_type(self):
        return self.settings['cursor_type']

    @property
    def autocommit(self):
        return self.settings['autocommit']
