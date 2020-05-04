from enum import Enum


class RestoreType(Enum):
    DBUP_SCRIPTS = 1
    SINGLE_SCRIPT = 2
    TAR_BACKUP = 3


class TestDataInsert(Enum):
    NONE = 1
    FROM_SCRIPT = 2
    IN_BACKUP = 3


class CursorType(Enum):
    Default = 1
    DictCursor = 2
