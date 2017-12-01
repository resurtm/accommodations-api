from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.from_object('accommodations.settings')
app.config.from_envvar('APP_SETTINGS')

mongo = PyMongo(app)
CORS(app, origins=app.config['CORS_ORIGINS'])


@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'application/json'
    return response


# noinspection PyUnresolvedReferences
import accommodations.views.auth  # noqa
# noinspection PyUnresolvedReferences
import accommodations.views.common  # noqa
# import accommodations.views.project
