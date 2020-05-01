class TestSuit:
    # setting up testing suit, before tests
    # in config: either from backup, or, if not supplied,
    # from dbup script structure
    @classmethod
    def setup(cls, **kwargs):
        pass

    # cleaning up after tests or if tests fail
    @classmethod
    def teardown(cls, **kwargs):
        pass

    # resets schemas in database, according to config
    # pg_restore with schema cleaning
    @classmethod
    def reset(cls, **kwargs):
        pass
