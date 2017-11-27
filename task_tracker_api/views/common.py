from task_tracker_api.decorators import jsonified
from task_tracker_api.main import app


@app.route('/v1/guest-ping', methods=['POST'])
@jsonified
def guest_ping(json):
    return '', {'data': json}


@app.route('/v1/auth-ping', methods=['POST'])
@jsonified
def auth_ping(json):
    return '', {'data': json}
