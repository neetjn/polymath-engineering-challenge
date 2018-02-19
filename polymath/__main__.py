import argparse
import json
import os

import jinja2

from polymath.api import api
from polymath.constants import API_HOST, API_PORT
from polymath.core import get_categories_from_ebay, get_category
from polymath.db import bootstrap, drop_database, Category
from polymath.mediatypes import CategoryDtoSerializer
from polymath.utils import to_json


def rebuild():
    """Bootstrap application"""
    drop_database()
    categories = get_categories_from_ebay()
    bootstrap(categories)

def render(category_id):
    """
    Renders an interactive view for the desired category using Jinja.

    :param category_id: Identifier for target category.
    :type category_dto: str
    """
    try:
        category = get_category(category_id, tree=False)
    except Category.DoesNotExist:
        print(f'No category with id: {category_id}')
    else:
        fs = jinja2.FileSystemLoader(os.path.dirname(os.path.abspath(__file__)))
        tpl = jinja2\
            .Environment(loader=fs, trim_blocks=True)\
            .get_template('./templates/categories.j2')\
            .render(category=category, data=json.dumps(to_json(CategoryDtoSerializer, category)))

        dest = open(f'{category_id}.html', 'w')
        dest.write(tpl)


def payload(category_id):
    """Dump category tree payload from category id"""
    try:
        category = get_category(category_id, tree=True)
    except Category.DoesNotExist:
        print(f'No category with id: {category_id}')
    else:
        pl = open(f'{category_id}.json', 'w')
        pl.write(json.dumps(to_json(CategoryDtoSerializer, category), sort_keys=True, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('--rebuild', action='store_true', help='Rebuild categories.')
    a.add_argument('--render', help='Render category tree.', type=int)
    a.add_argument('--json', help='Dump category tree as JSON payload.', type=int)
    a.add_argument('--app', action='store_true', help='Start rest api.')
    args, remaining_args = a.parse_known_args()
    if args.rebuild:
        rebuild()
    if args.render:
        render(args.render)
    if args.json:
        payload(args.json)
    if args.app or (not args.rebuild and not args.render and not args.json):
        api.run(host=API_HOST, port=int(API_PORT), threaded=True, processes=1)
