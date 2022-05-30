import os


class Config(object):
    SECRET_URI = os.environ.get("mongodb://localhost:27017/client") or "mongodb://localhost:27017/client"