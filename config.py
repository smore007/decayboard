import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'KEK'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    IMGUR_ID = '4e8608bc58aa224'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Post.sqlite3'
