from typing import TypeVar, Type
from .conf import PG_Config

T = TypeVar('T')


class Query:
    # execute no return query
    @classmethod
    def execute(cls, query: str, params: dict = None, model_type: Type[T] = None,
                local_config_override: PG_Config = None):
        pass

    # execute query returning multiple results
    @classmethod
    def fetch(cls, query: str, params: dict = None, model_type: Type[T] = None,
              local_config_override: PG_Config = None):
        pass

    # execute query returning single result
    @classmethod
    def fetch_first(cls, query: str, params: dict = None, model_type: Type[T] = None,
                    local_config_override: PG_Config = None):
        pass
