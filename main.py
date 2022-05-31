# I used localhost mongodb

import flask
from flask import Flask, render_template, request, jsonify, url_for
from flask_pymongo import PyMongo
from bson.json_util import dumps
from werkzeug.utils import redirect
from config import Config
import json

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
app.config.from_object(Config)
mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route("/")
def add_user():
    db.users.insert_one({'name': 'Root', 'age': 25})
    message = flask.jsonify(message="success")
    return message


# IF YOU WANNA USE HTML INTERFACE, USE THIS BLOCK
################################################################
# @app.route("/", methods=['get', 'post'])
# def add_user():
#     user_name = ''
#     user_age = ''
#
#     if request.method == 'POST':
#         user_name = request.form.get('name')
#         user_age = request.form.get('age')
#     if user_name and user_age:
#         db.users.insert_one({'name': user_name, 'age': user_age})
#         message = flask.jsonify(message="success")
#         return render_template('add_user.html', message=message)
#     return render_template('add_user.html')
##################################################################


@app.route("/find_user/<user_name>", methods=['get', 'post'])
def find_user(user_name):
    users = db.users.find({'name': user_name})
    user = dumps(users)
    return user


# IF YOU WANNA USE HTML INTERFACE, USE THIS BLOCK
################################################################
# @app.route("/find_user", methods=['get', 'post'])
# def find_user_get():
#     user_name = request.form.get('name')
#     user = db.users.find({'name': user_name})
#     json_name = dumps(user)
#     data = json.loads(json_name)
#     jom = {}
#     for i in data:
#         jom[i['name']] = jom.get(i['name'], i['age'])
#     return render_template('find_user.html', jom=jom)
##################################################################


@app.route("/replace_user/<user_name>")
def replace_user(user_name):
    user = db.users.find_one_and_replace({'name': user_name}, {'name': 'Jura'})
    return dumps(user)


@app.route("/update_user/<user_name>")
def update_user(user_name):
    user = db.users.find_one_and_update({'name': user_name}, {"$set": {'age': 50}})
    return dumps(user)


@app.route("/delete_user/<user_name>")
def delete_user(user_name):
    user = db.users.find_one_and_delete({'name': user_name})
    if user is not None:
        return dumps(user)
    return "Name does not exist"


if __name__ == "__main__":
    app.run()
