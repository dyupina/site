import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '20d59d54d9a34d9e764707489a28f20b'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'