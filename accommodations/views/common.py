from accommodations.decorators import jsonified, jwt_auth
from accommodations.main import app


@app.route('/v1/ping/guest', methods=['POST'])
@jsonified
def guest_ping(json):
    return 'Ping success', json


@app.route('/v1/ping/auth', methods=['POST'])
@jwt_auth()
@jsonified
def auth_ping(json):
    return 'Ping success', json
