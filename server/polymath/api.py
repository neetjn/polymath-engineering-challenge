
from flask import Flask, Response, redirect, request, url_for
from flask_cors import CORS
from flask_responses import json_response

from polymath.core import get_category, get_categories, category_to_dto
from polymath.mediatypes import CategoryDtoSerializer, LinkDto
from polymath.utils import to_json


api = Flask(__name__)
CORS(api, resources={r'/api/*': {'origins': '*'}})


# would ideally cache with redis, using sqlite pragma
# assuming we don't provide an interface to modify, add, or remove resources
# we only actually need to reference the entire tree once

cached_categories_dto = None
cached_category_dtos = []


@api.route('/api/v1/categories/', methods=['GET'])
def get_categories_resource():
    """Endpoint for fetching categories from the top level down."""
    cached_categories = cached_categories or get_categories()
    categories = cached_categories
    return json_response(json.loads([to_json(CategoryDtoSerializer, category) for category in categories])


@api.route('/api/v1/category/<category_id>', methods=['GET'])
def get_category_resource(category_id):
    """Endpoint for fetching category by id, including children."""
    category = next((c for c in cached_category_dtos if c.category_id == category_id), None) or get_category(category_id)
    return json_response(to_json(CategoryDtoSerializer, category))
