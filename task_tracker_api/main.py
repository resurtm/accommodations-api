from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.from_object('task_tracker_api.settings')
app.config.from_envvar('TASK_TRACKER_API_SETTINGS')

mongo = PyMongo(app)


@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'application/json'
    return response


# noinspection PyUnresolvedReferences
import task_tracker_api.views
