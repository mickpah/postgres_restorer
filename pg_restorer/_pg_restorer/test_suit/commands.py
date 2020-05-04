from typing import Dict

from pg_restorer._pg_restorer.utils import run_command


def dropdb(dbname: str, env_vars: Dict):
    run_command(
        ['dropdb', '--if-exists', dbname],
        env_vars=env_vars
    )


def createdb(dbname: str, env_vars: Dict):
    run_command(
        ['createdb', dbname],
        env_vars=env_vars
    )


def pg_dump(dbname: str, tar_name: str, env_vars: Dict):
    run_command(
        ['pg_dump', '-s', '-F', 't', dbname, tar_name],
        env_vars=env_vars
    )


def pg_restore(dbname: str, tar_name: str, env_vars: Dict):
    run_command(
        ['pg_restore', '-c', '--if-exists', '-d', dbname, tar_name],
        env_vars=env_vars
    )
