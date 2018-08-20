''' import modules '''
import re
from flask import jsonify, request
from stackoverflowlite.views import api
from stackoverflowlite.models.users import User, cur

email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"


@api.route('/signup', methods=['POST'])
def sign_up():
    email = request.get_json('email')['email']
    password = request.get_json('password')['password']
    username = request.get_json('username')['username']
    cur.execute("select * from users where email = '{}'".format(email))
    emails = cur.fetchall()
    cur.execute("select * from users where username = '{}'".format(username))
    names = cur.fetchall()

    if len(emails) > 0:
        response = jsonify({"message": "User already exists"})
        response.status_code = 409
        return response

    if len(names) > 0:
        response = jsonify({"message": "Username is taken"})
        response.status_code = 409
        return response

    if not email or email == " ":
        response = jsonify({"message": "Email not provided"})
        response.status_code = 400
        return response

    if not re.match(email_format, email):
        return jsonify({"message": "incorrect email format"})

    if not password or password == " ":
        response = jsonify({"message": "Password not provided"})
        response.status_code = 400
        return response

    if not username or username == " ":
        response = jsonify({"message": "Username not provided"})
        response.status_code = 400
        return response

    if not request.json:
        response = jsonify({"message": "Incorrect request format"})
        response.status_code = 400
        return response

    User(str(email), str(password), str(username))
    cur.execute("select * from users where username = '{}'".format(username))
    entries = cur.fetchall()
    return jsonify({"User": entries})


@api.route('/login', methods=['POST'])
def login():
    email = request.get_json('email')['email']
    print(email)
    password = request.get_json('password')['password']
    print(password)

    if not email or email == " ":
        response = jsonify({"message": "Email not provided"})
        response.status_code = 400
        return response

    if not re.match(email_format, email):
        response = jsonify({"message": "incorrect email format"})
        response.status_code = 400
        return response

    if not password or password == " ":
        response = jsonify({"message": "Password not provided"})
        response.status_code = 400
        return response

    if not request.json:
        response = jsonify({"message": "Invalid request format"})
        response.status_code = 400
        return response

    cur.execute("select password from users where email = '{}'".format(email))
    correct_password = cur.fetchall()
    print(correct_password)
    cur.execute("select email from users where email = '{}'".format(email))
    correct_email = cur.fetchall()

    if len(correct_email) == 0:
        response = jsonify({"message": "email is incorrect"})
        return response
    if correct_password[0][0] != password:
        response = jsonify({"message": "password is incorrect"})
        return response
    else:
        """cur.execute("select password from users where email = '{}'".format(email))
        user_exists = cur.fetchall()
        if user_exists:
            try:
                jwt_token = user_exists.generate_jwt(user_exists.user_id)

                response = jsonify({
                    "message": "Log in successful",
                    "jwt": jwt_token.decode('utf-8')
                })
                response.status_code = 200
                return response
            except Exception as e:
                response = jsonify({
                    "message": "User could not be logged in",
                    "error": str(e)
                })

                response.status_code = 202
                return response"""
        return jsonify({"message": "logged in successfully"})
