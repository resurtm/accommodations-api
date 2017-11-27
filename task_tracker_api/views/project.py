import json

from flask import jsonify, request

from task_tracker_api.main import app
from task_tracker_api.tools import validate_json


@app.route('/v1/project', methods=['POST'])
def create():
    data = json.loads(request.data.decode('utf-8', 'strict'))
    if not validate_json(data, 'project'):
        return jsonify({'ok': False,
                        'msg': 'Unable to validate project data'}), 400
    return jsonify({'ok': True, 'msg': ''})


@app.route('/v1/project', methods=['DELETE'])
def delete():
    return jsonify({'ok': True, 'msg': ''})


@app.route('/v1/project', methods=['PUT'])
def update():
    return jsonify({'ok': True, 'msg': ''})


@app.route('/v1/project', methods=['GET'])
def fetch_projects():
    return jsonify({'ok': True, 'msg': ''})


@app.route('/v1/project/<id>', methods=['GET'])
def fetch_project(id):
    return jsonify({'ok': True, 'msg': ''})
