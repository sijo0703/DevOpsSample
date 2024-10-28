from flask import Blueprint

# Define the blueprint for web
web = Blueprint('web', __name__)

from . import web_app