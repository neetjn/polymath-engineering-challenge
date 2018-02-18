
from flask import Flask, Response, redirect, request, url_for
from flask_cors import CORS
from flask_responses import json_response

from grio.core import get_people, get_person, create_person, delete_person, update_person
from grio.mediatypes import PersonDtoSerializer, PeopleDtoSerializer, LinkDto


app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': '*'}})

@trace
