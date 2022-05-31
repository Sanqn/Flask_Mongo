import os


class Config(object):
    MONGO_URI = os.environ.get("mongodb://localhost:27017/users") or "mongodb://localhost:27017/users"