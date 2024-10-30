import os
import signal

from flask import Blueprint, render_template, request, redirect, url_for
import pymysql
from app.blueprints.main.db_connector import get_db_connection
from . import rest


@rest.route('/add_user', methods=['GET', 'POST'])
def add_user():
    connection = get_db_connection()
    if connection is None:
        return "Database connection error", 500
    if request.method == 'POST':
        user_id = request.form['userid']
        user_name = request.form['username']
        creation_date = request.form['creationdate']
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (user_id, user_name, creation_date) VALUES (%s, %s, %s)", (user_id, user_name, creation_date))
                connection.commit()
            return redirect(url_for('web.index'))
        except pymysql.Error as e:
            print(f"Error inserting user into db: {e}")
            return "Error inserting user into db", 500
        finally:
            connection.close()
    return render_template('add_user.html', action="Add User")


@rest.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    connection = get_db_connection()
    if connection is None:
        return "Database connection error", 500
    if request.method == 'POST':
        user_name = request.form['username']
        creation_date = request.form['creationdate']
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE users SET user_name = %s, creation_date = %s WHERE user_id = %s", (user_name, creation_date, user_id))
                connection.commit()
            return redirect(url_for('web.index'))
        except pymysql.Error as e:
            print(f"Error updating user from db: {e}")
            return "Error updating user from db", 500
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
    except pymysql.Error as e:
        print(f"Error retrieving user from db: {e}")
        return "Error retrieving user from db", 500
    finally:
            connection.close()
    return render_template('edit_user.html', user=user, action="Edit User")


@rest.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    connection = get_db_connection()
    if connection is None:
        return "Database connection error", 500
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            connection.commit()
    except pymysql.Error as e:
        print(f"Error deleting user from db: {e}")
        return "Error deleting user from db", 500
    finally:
        connection.close()
    return redirect(url_for('web.index'))

@rest.route('/stop_server')
def stop_server():
    os.kill(os.getpid(),signal.CTRL_C_EVENT)
    return 'Server Stopped'

# use GET request to retrieve a user details based on the user_id provided if not display user not found