from flask import Flask
from app.blueprints.main.db_connector import create_table  # Import the create_table function

# Import the blueprints

from app.blueprints.main import main as main_blueprint
from app.blueprints.rest import rest as rest_blueprint
from app.blueprints.web import web as web_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Register blueprints, routes, etc.
    app.register_blueprint(main_blueprint)
    app.register_blueprint(rest_blueprint)
    app.register_blueprint(web_blueprint)

    # Call create_table() to ensure the table is created
    create_table()

    return app


