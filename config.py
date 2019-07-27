import os


class Config(object):
    API_VERSION = '1.0.0'
    API_TITLE = 'Ithaca'
    API_DESCRIPTION = '멘토가 있는 교실, 이타카'

    JWT_TOKEN_LOCATION = 'headers'
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_SECRET_KEY = os.urandom(24)
    MONGO_URI = ''


class DevConfig(Config):
    HOST = 'localhost'
    PORT = 5000
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DB = 'test'
