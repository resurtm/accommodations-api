from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.from_object('task_tracker_api.settings')
app.config.from_envvar('TASK_TRACKER_API_SETTINGS')

mongo = PyMongo(app)

# noinspection PyUnresolvedReferences
import task_tracker_api.views