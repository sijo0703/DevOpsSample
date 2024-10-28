from flask import Blueprint, render_template, request, redirect, url_for
import pymysql
import app.blueprints.main.db_connector
from app.blueprints.main.db_connector import get_db_connection
from app.blueprints.web import web as web_blueprint
from . import web

#web = Blueprint('web', __name__)

@web.route('/')
def index():
    connection = get_db_connection()
    if connection is None:
        return "Database connection error", 500
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return render_template('index.html', users=users)
    except pymysql.Error as e:
        print(f"Error fetching users: {e}")
        return "Error fetching users", 500
    finally:
        connection.close()