from psycopg2 import connect
from pg_restorer._pg_restorer.enums import CursorType
from pg_restorer._pg_restorer.exceptions import PG_ConnectionError
from pg_restorer._pg_restorer.strategies import cursor_strategy
from pg_restorer._pg_restorer.utils import dict_to_str


class PG_Connection(object):
    def __init__(self, connection_string: str, cursor_type: CursorType, autocommit: bool):
        self.connection_string = connection_string
        self.cursor_type = cursor_type
        self.autocommit = autocommit
        self._cursor = None
        self.connection = None

    def __repr__(self):
        _repr = self.connection.get_dsn_parameters() if \
            self.connection else None
        return dict_to_str(_repr) if _repr else ''

    def __enter__(self):
        self.connection = connect(
            dsn=self.connection_string,
            cursor_factory=cursor_strategy[self.cursor_type]
        )
        self.connection.autocommit = self.autocommit
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type and self.autocommit:
            self.connection.commit()
            self.connection.close()
        else:
            self.connection.rollback()
            self.connection.close()

            traceback_details = {
                'filename': exc_tb.tb_frame.f_code.co_filename,
                'lineno': exc_tb.tb_lineno,
                'name': exc_tb.tb_frame.f_code.co_name,
                'type': exc_type.__name__,
                'message': exc_val.pgerror,
                'pg_code': exc_val.pgcode
            }

            raise PG_ConnectionError(traceback_details)
