import os

from .enums import RestoreType, TestDataInsert, CursorType

DEFAULT_SETTINGS = {
    'connection_info': {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'postgres',
        'main_db': 'postgres'
    },
    'test_db_name': 'test_database',
    'restore_type': RestoreType.DBUP_SCRIPTS,
    'insert_test_data': TestDataInsert.FROM_SCRIPT,
    'workdir': os.getcwd(),
    'restore_path': '',
    'data_path': '',
    'cursor_type': CursorType.Default,
    'autocommit': False
}