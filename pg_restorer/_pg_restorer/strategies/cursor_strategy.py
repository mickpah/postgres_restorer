from psycopg2.extras import DictCursor

from pg_restorer._pg_restorer.enums import CursorType

cursor_strategy = {
    CursorType.Default: None,
    CursorType.DictCursor: DictCursor
}
