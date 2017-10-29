from os import path as p

DEBUG = False
SECRET_KEY = '!!! CHANGE THIS !!!'

MONGO_DBNAME = 'task_tracker'

JSON_SCHEMA_PATH = p.join(p.dirname(p.abspath(__file__)), 'json_schema')
