from .enums import RestoreType, TestDataInsert, CursorType

DEFAULT_SETTINGS = {
    'server_connection_string': 'host=localhost user=postgres password=postgres',
    'test_db_name': 'test_database',
    'restore_type': RestoreType.DBUP_SCRIPTS,
    'insert_test_data': TestDataInsert.FROM_SCRIPT,
    'workdir': '',
    'restore_path': '',
    'data_path': '',
    'cursor_type': CursorType.Default,
    'autocommit': True
}
