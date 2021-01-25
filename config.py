import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'KEK'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('postgres://nxytkuntklroyq:7e6e9d6b13d74757499a34c4774f2025b50e3d34fbdd102b2c7fa091ec9ceea6@ec2-54-82-208-124.compute-1.amazonaws.com:5432/d74lh90jcnvjl6')


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Post.sqlite3'