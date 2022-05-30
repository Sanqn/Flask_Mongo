import flask
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from config import Config
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
mongodb_client = PyMongo(app)
db = mongodb_client.db

@app.route("/", methods=['get', 'post'])
def add_user():
    user_name = ''
    user_age = ''

    if request.method == 'POST':
        user_name = request.form.get('name')
        user_age = request.form.get('age')
    if user_name and user_age:
        db.users.insert_one({'name': user_name, 'age': user_age})
        message = flask.jsonify(message="success")
        return render_template('add_user.html', message=message)
    return render_template('add_user.html')
    # db.users.insert_one({'name': 'Joombo', 'age': 25})
    # message = flask.jsonify(message="success")
    # return render_template('add_user.html', message=message)

# @app.route("/find_user", methods=['get', 'post'])
# def find_user_get():
#     user_name = request.form.get('name')
#     user = db.users.find({'name': user_name})
#     json_name = dumps(user)
#     data = json.loads(json_name)
#     for i in data:
#         name = i['name']
#         age = i['age']
#         return render_template('find_user.html', name=name, age=age)

@app.route("/find_user/<user_name>", methods=['get', 'post'])
def find_user_get(user_name):
    users = db.users.find({'name': user_name})
    user = dumps(users)
    return user



if __name__ == "__main__":
    app.run()
