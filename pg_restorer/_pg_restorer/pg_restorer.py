from .conf import PG_Config
from .query import Query
from .test_suit import TestSuit


class PG_Restorer:
    def __init__(self, config: PG_Config):
        self._config = config
        self.query = Query
        self.test_suit = TestSuit

    # returns connection info
    def __repr__(self):
        pass


def get_new_db(config: PG_Config) -> PG_Restorer:
    return PG_Restorer(config)
