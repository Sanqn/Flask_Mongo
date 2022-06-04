# I used localhost mongodb
import flask
from flask import Flask, render_template, request, jsonify, url_for
from flask_pymongo import PyMongo
from bson.json_util import dumps
from werkzeug.utils import redirect
from config import Config
import json
from werkzeug.security import generate_password_hash

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
app.config.from_object(Config)
mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route("/", methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    password = data['pwd']
    email = data['email']

    if name and email and password and request.method == 'POST':
        hash_pass = generate_password_hash(password)
        db.users.insert_one({'name': name, 'email': email, 'pwd': hash_pass})
        message = flask.jsonify(message="success")
        return message


# IF YOU WANNA USE HTML INTERFACE(CREATE USER), USE THIS BLOCK
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


# IF YOU WANNA USE HTML INTERFACE(FIND USER), USE THIS BLOCK
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


@app.route("/replace_user/<user_name>/", methods=['PUT'])
def replace_user(user_name):
    name = user_name
    data = request.json
    email = data['email']
    password = data['pwd']

    if name and email and password and request.method == 'PUT':
        has_pass = generate_password_hash(password)
        db.users.ind_one_and_replace({'name': name}, {"$set": {'email': email, 'pwd': has_pass}})
        resp = jsonify(message='Update successfully')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route("/update_user/<user_name>", methods=['PUT'])
def update_user(user_name):
    name = user_name
    data = request.json
    email = data['email']
    password = data['pwd']

    if name and email and password and request.method == 'PUT':
        has_pass = generate_password_hash(password)
        db.users.find_one_and_update({'name': name}, {"$set": {'email': email, 'pwd': has_pass}})
        resp = jsonify(message='Update successfully')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route("/delete_user/<user_name>", methods=['DELETE'])
def delete_user(user_name):
    user = db.users.find_one_and_delete({'name': user_name})
    if user is not None:
        return dumps(user)
    return "Name does not exist"


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(debug=True)
