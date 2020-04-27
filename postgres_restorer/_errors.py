from typing import Dict


class PostgresRestorerError(Exception):
    def __init__(self, message: str = None, payload: Dict[str, str] = None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload
