from flask import Blueprint

# Define the blueprint for rest
rest = Blueprint('rest', __name__)

from . import rest_app