from contextlib import contextmanager
from typing import Dict
from .pg_restorer import PG_Restorer
from .enums import RestoreType, TestDataInsert, CursorType


def get_new_db(settings: Dict) -> PG_Restorer:
    return PG_Restorer(settings)

