# collection on functions used everywhere
from typing import List
from psycopg2 import connect


def flatten_list_of_lists(list_of_lists: List[List]):
    return [y for x in list_of_lists for y in x]


# return psycopg2 connection
def get_connection(*arg):
    return connect(*arg)
