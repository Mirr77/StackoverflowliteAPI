from functools import wraps
from flask import jsonify, request
import jwt
from db.dbconfig import open_connection, close_connection


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
        conn = open_connection()
        cur = conn.cursor()
        blacklisted = cur.execute("select token from blacklist where token = '{}'".format(str(jwt_token)))

        if blacklisted:
            response = jsonify({
                "message": "Account logged out. Please log in to continue"
            })
            response.status_code = 401
            cur.close()
            close_connection(conn)
            return response

        try:
            identity = jwt.decode(jwt_token, 'secret')['sub']
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

  
