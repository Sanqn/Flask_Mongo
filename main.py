import flask
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from config import Config

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



@app.route("/find_user/<name>")
def find_user(name):
    user = db.users.find({'name': name})
    name = request.form.get()
    return render_template('add_user.html', user=dumps(user))



if __name__ == "__main__":
    app.run()
