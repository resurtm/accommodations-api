from accommodations.decorators import jsonified, jwt_auth
from accommodations.main import app


@app.route('/v1/guest-ping', methods=['POST'])
@jsonified
def guest_ping(json):
    return '', {'data': json}


@app.route('/v1/auth-ping', methods=['POST'])
@jwt_auth
@jsonified
def auth_ping(json):
    return '', {'data': json}
