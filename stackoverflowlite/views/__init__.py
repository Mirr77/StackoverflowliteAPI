from flask import Blueprint,jsonify

api = Blueprint('api', __name__)


@api.route('/')
@api.route('/home')
def index():
    ''' The API's base route '''
    response = jsonify({
        "Message": "Welcome to stackoverflowliteAPI"
    })
    response.status_code = 200
    return response