
from flask import Flask, Response, redirect, request, url_for
from flask_cors import CORS
from flask_responses import json_response

from polymath.core import get_category, get_categories
from polymath.mediatypes import CategoryDtoSerializer, CategoriesDtoSerializer, LinkDto


api = Flask(__name__)
CORS(api, resources={r'/api/*': {'origins': '*'}})


@app.route('/api/v1/categories/', methods=['GET'])
def get_categories_resource():
    """
    """
    pass


@app.route('/api/v1/category/<category_id>', methods=['GET'])
def get_categories_resource(category_id):
    """
    """
    pass
