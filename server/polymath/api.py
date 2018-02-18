
from flask import Flask, Response, redirect, request, url_for
from flask_cors import CORS
from flask_responses import json_response

from polymath.core import get_summary, get_categories, get_category
from polymath.mediatypes import CategoryDtoSerializer, CategoryCollectionDtoSerializer, LinkDto
from polymath.utils import to_json


api = Flask(__name__)
CORS(api, resources={r'/api/*': {'origins': '*'}})


# would ideally cache with redis, using sqlite pragma
# assuming we don't provide an interface to modify, add, or remove resources
# we only actually need to reference the entire tree once

cached_category_summary = None
cached_category_collection = None
cached_category_dtos = []

@api.route('/api/v1/summary/', methods=['GET'])
def get_summary_resource():
    """Endpoint for fetching topmost categories."""
    global cached_category_summary

    category_summary = cached_category_summary
    if not category_summary:
        category_summary = get_summary()
        category_summary.links = [
            LinkDto(href=url_for('get_categories_resource'), rel='categories'),
            LinkDto(href=url_for('get_summary_resource'), rel='summary')
        ]
        for category in category_summary.categories:
            category.links = [LinkDto(href=url_for('get_category_resource', category_id=category.category_id))]
        cached_category_summary = category_summary

    return json_response(to_json(CategoryCollectionDtoSerializer, category_summary))


@api.route('/api/v1/categories/', methods=['GET'])
def get_categories_resource():
    """Endpoint for fetching categories from the top level down."""
    global cached_category_collection

    category_collection = cached_category_collection or get_categories()
    if not cached_category_collection:
        category_collection.links = [
            LinkDto(href=url_for('get_categories_resource'), rel='categories'),
            LinkDto(href=url_for('get_summary'), rel='summary')
        ]
        cached_category_collection = category_collection
    return json_response(to_json(CategoryCollectionDtoSerializer, category_collection))


@api.route('/api/v1/category/<category_id>', methods=['GET'])
def get_category_resource(category_id):
    """Endpoint for fetching category by id, including children."""
    category = next((c for c in cached_category_dtos if c.category_id == category_id), None)
    if not category:
        category = get_category(category_id)
        category.links = [LinkDto(href=url_for('get_category_resource', category_id=category_id), rel='self')]
        cached_categories_dto.append(category)
    return json_response(to_json(CategoryDtoSerializer, category))
