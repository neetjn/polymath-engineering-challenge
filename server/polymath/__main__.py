import argparse
import os

from polymath.api import api
from polymath.constants import API_HOST, API_PORT
from polymath.core import get_categories_from_ebay, get_category, render_category
from polymath.db import bootstrap, drop_database, Category


def rebuild():
    """Bootstrap application"""
    drop_database()
    categories = get_categories_from_ebay()
    bootstrap(categories)


def render(category_id):
    """Render category tree from category id"""
    tpl = open('Output.txt', 'w')
    try:
        category = get_category(category_id)
    except Category.DoesNotExist:
        print(f'No category with id: {category_id}')
    else:
        tpl.write(render_category())


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--rebuild', action='store_true', help='Rebuild categories.')
    a.add_argument('--render', help='Render category tree.')
    args, remaining_args = a.parse_known_args()
    if args.rebuild:
        rebuild()
    if args.render:
        render(args.render)
    if not args.rebuild and not args.render:
        api.run(host=API_HOST, port=int(API_PORT), threaded=True, processes=1)
