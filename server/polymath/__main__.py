import argparse

from polymath.core import get_categories_from_ebay
from polymath.db import bootstrap, drop_database

def rebuild():
    """Bootstrap application"""
    drop_database()
    categories = get_categories_from_ebay()
    bootstrap(categories)


def render(category):
    pass


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--rebuild', action='store_true', help='Rebuild categories.')
    a.add_argument('--render', help='Render category tree.')
    a.add_argument('--app', help='Start api.')
    args, remaining_args = a.parse_known_args()

    if args.rebuild:
        rebuild()
