from typing import Dict

from .connectors.connector import Connector
from .default_settings import DEFAULT_SETTINGS


class PG_Restorer:
    def __init__(self, config: Dict):
        self._pg_config = DEFAULT_SETTINGS
        self._pg_config.update(config)

    def test(self):
        return Connector(self.pg_config)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    # returns current settings
    def __repr__(self):
        return str(self.pg_config)

    @property
    def pg_config(self):
        return self._pg_config

    @pg_config.setter
    def pg_config(self, value):
        self._pg_config = value
