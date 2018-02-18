
from flask import Flask, Response, redirect, request, url_for
from flask_cors import CORS
from flask_responses import json_response

from polymath.core import get_category, get_categories, category_to_dto
from polymath.mediatypes import CategoryDtoSerializer, LinkDto


api = Flask(__name__)
CORS(api, resources={r'/api/*': {'origins': '*'}})


# would ideally cache with redis
# assuming we don't provide an interface to modify, add, or remove resources
# we only actually need to reference the entire tree once
cached_category_tree = None


@api.route('/api/v1/categories/', methods=['GET'])
def get_categories_resource():
    """
    Endpoint for fetching categories from the top level down.
    """
    categories = get_categories()


@api.route('/api/v1/category/<category_id>', methods=['GET'])
def get_category_resource(category_id):
    """
    Endpoint for fetching
    """
    pass
