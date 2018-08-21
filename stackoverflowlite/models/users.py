import jwt
from datetime import datetime,timedelta
from passlib.apps import custom_app_context as pwd_hash
from db.dbconfig import open_connection, close_connection
from flask import jsonify


class User(object):
    ''' User model '''

    def __init__(self, email, password):
        ''' Initialize user '''
        self.email = email
        self.password = password

    def user_exists(self):
        """ Check if a user exists in the db """
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * from users WHERE email='{}'".format(self.email))
        user = cur.fetchone()
        cur.close()
        close_connection(conn)
        return user

    def user_info(self):
        """ Return user info in a dictionary """
        user = self.user_exists()

        if user:
            user_obj = {}
            user_obj['user_id'] = user[0]
            user_obj['email'] = user[1]

            return user_obj

        else:
            response = jsonify({
                "message": "The user does not exist"
            })
            response.status_code = 401
            return response

    def signup(self, username):
        """ Register a new user """
        user_exists = self.user_exists()

        if user_exists:
            response = jsonify({
                "message": "An account with that email already exists"
            })
            response.status_code = 409
            return response

        else:
            hashed_pw = pwd_hash.encrypt(self.password)
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES('{}', '{}', '{}')"
                        .format(username, self.email, hashed_pw))
            cur.close()
            close_connection(conn)

            token = self.generate_jwt(user_exists[0])

            user_info = self.user_info()
            response = jsonify({
                "message": "User registered successfully",
                "token": token.decode("utf-8"),
                "user": user_info
            })
            response.status_code = 200
            return response

    def login(self):
        """ Log in existing user """
        user_exists = self.user_exists()
        print(user_exists)

        if user_exists:
            pw_match = self.verify_pwd(user_exists[3])

            if pw_match:
                token = self.generate_jwt(user_exists[0])

                user_info = self.user_info()

                response = jsonify({
                    "message": "Login successful",
                    "token": token.decode("utf-8"),
                    "user": user_info
                })
                response.status_code = 200
                return response

            else:
                response = jsonify({
                    "message": "Wrong password"
                })
                response.status_code = 401
                return response

        else:
            response = jsonify({
                "message": "The email you entered does not match any of our records"
            })
            response.status_code = 401
            return response

    def verify_pwd(self, stored_pwd):
        """ Confirm that the given password matches the one stored in db """
        return pwd_hash.verify(self.password, stored_pwd)

    def generate_jwt(self, user_id):
        """ Generate an authentication token for the user """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                'SECRET_KEY',
                algorithm='HS256'
            )
        except Exception as e:
            return e


