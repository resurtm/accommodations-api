from os import path as p

DEBUG = False

SECRET_KEY = '!!! CHANGE THIS !!!'
JWT_SECRET_KEY = '!!! CHANGE THIS !!!'
CORS_ORIGINS = []

MONGO_DBNAME = 'accommodations'

JSON_SCHEMA_PATH = p.join(p.dirname(p.abspath(__file__)), 'json_schema')
