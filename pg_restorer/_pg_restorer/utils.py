# collection on functions used everywhere
import os
import subprocess
from typing import List, Dict


def flatten_list_of_lists(list_of_lists: List[List]):
    return [y for x in list_of_lists for y in x]


def build_schema_from_dbup(scripts_path: str) -> str:
    folders = sorted(os.listdir(scripts_path))
    subscripts = []

    for folder in folders:
        scripts = sorted(
            os.listdir(
                os.path.join(scripts_path, folder))
        )
        for script in scripts:
            file_path = os.path.join(scripts_path, folder, script)

            with open(file_path, 'r') as file:
                subscripts.append(file.read())

    return ''.join(subscripts)


def dict_to_str(dictionary: Dict, separator: str = '\n') -> str:
    string = separator.join([f'{k}: {v}' for k, v in dictionary.items()])
    return f'\n{string}'


def run_command(command: List, env_vars: Dict):
    my_env = os.environ
    my_env.update(env_vars)
    subprocess.Popen(command, env=env_vars)
