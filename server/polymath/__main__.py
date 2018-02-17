import argparse

import polymath.core
import polymath.db


def rebuild():
    """Bootstrap application"""
    db.drop_database()
    categories = core.get_categories()
    db.bootstrap(categories)


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--rebuild', help='Rebuild categories.')
    a.add_argument('--render', help='Render category tree.')
    a.add_argument('--app', help='Start api.')
    args, remaining_args = a.parse_known_args()

    print(args)
