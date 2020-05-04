class TestSuit:
    # setting up testing suit, before tests
    # in config: either from backup, or, if not supplied,
    # from dbup script structure
    def setup(self):
        pass
    
    # cleaning up after tests or if tests fail
    def teardown(self, **kwargs):
        pass

    # resets schemas in database, according to config
    # pg_restore with schema cleaning
    def reset(self, **kwargs):
        pass
