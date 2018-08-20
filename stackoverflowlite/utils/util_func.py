from functools import wraps
from flask import jsonify, request
import jwt
import config
from stackoverflowlite.models.blacklist import Blacklist


# Authorization middleware
def requires_auth(func):
    ''' Decorator to secure private routes '''

    @wraps(func)
    def authorize(*args, **kwargs):
        ''' Check for the user's authentication token in header '''

        if 'Authorization' not in request.headers:
            response = jsonify({
                "message": "Missing Authorization header"
            })
            response.status_code = 401
            return response

        jwt_token = request.headers['Authorization'].encode('ascii', 'ignore')
        blacklisted = Blacklist.query.filter_by(token=str(jwt_token)).first()

        if blacklisted:
            response = jsonify({
                "message": "Account logged out. Please log in to continue"
            })
            response.status_code = 401
            return response

        try:
            identity = jwt.decode(jwt_token, config.SECRET_KEY)['sub']
            return func(identity, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            response = jsonify({
                "message": "Your token has expired. Please log in to continue"
            })
            response.status_code = 401
            return response

        except jwt.InvalidTokenError:
            response = jsonify({
                "message": "Invalid token. Please log in or sign up to continue"
            })
            response.status_code = 401
            return response

    return authorize


