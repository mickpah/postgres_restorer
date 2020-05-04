import os
from typing import Dict
from ..connectors import Connector
import copy

from .commands import pg_restore, dropdb, createdb, pg_dump
from ..utils import build_schema_from_dbup
from ... import RestoreType


class TestSuit(Connector):
    def __init__(self, settings: Dict):
        self.test_suit_settings = copy.deepcopy(settings)
        self.test_suit_settings.update({'autocommit': True})
        _current_db = self.test_suit_settings['connection_info']['main_db']
        super().__init__(self.test_suit_settings, _current_db)

    # cleaning up after tests or if tests fail
    def teardown(self):
        dropdb(self.restore_db, self.env_vars)

    # resets schemas in database, according to config
    # pg_restore with schema cleaning
    def reset(self, **kwargs):
        pass

    def _setup_from_dbup_scripts(self, cursor):
        script = build_schema_from_dbup(self.test_suit_settings['restore_path'])
        cursor.execute(script)

    def _setup_from_single_script(self, cursor):
        with open(self.test_suit_settings['restore_path'], 'r') as file:
            script = file.read()
            cursor.execute(script)

    def _setup_from_tar_backup(self):
        pg_restore(self.restore_db, self.path_to_restore, self.env_vars)

    def setup(self):
        restore_mode = self.test_suit_settings['restore_type']

        dropdb(self.restore_db, self.env_vars)
        createdb(self.restore_db, self.env_vars)

        if restore_mode is RestoreType.SINGLE_SCRIPT:
            with self.cursor as _cursor:
                self._setup_from_single_script(_cursor)
        if restore_mode is RestoreType.DBUP_SCRIPTS:
            with self.cursor as _cursor:
                self._setup_from_dbup_scripts(_cursor)
        if restore_mode is RestoreType.TAR_BACKUP:
            self._setup_from_tar_backup()

        if restore_mode is not RestoreType.TAR_BACKUP:
            bak_db_name = os.path.join(
                self.settings['workdir'],
                f"{self.restore_db}.tar"
            )
            pg_dump(self.restore_db, bak_db_name, self.env_vars)

