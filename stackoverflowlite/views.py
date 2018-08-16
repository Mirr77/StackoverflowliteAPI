''' import modules '''
import re
from flask import jsonify, abort, make_response, request
from . import app
from .models.questions import questions, Question, Answer
from .models.users import User, users
email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"

@app.route('/stackoverflowlite/api/v1',methods=['GET'])
def index():
    return jsonify({"message":"Welcome to stackoverflowlite"})


@app.route('/stackoverflowlite/api/v1/questions', methods=['GET'])
def get_questions():
    ''' Get alll questions function '''
    return jsonify({'questions': [question for question in questions]})


@app.route('/stackoverflowlite/api/v1/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    ''' Get a question function '''
    question = [question for question in questions if question['question_id'] == question_id]
    if len(question) == 0:
        abort(404)
    return jsonify({'question': question[0]})

@app.route('/stackoverflowlite/api/v1/questions', methods=['POST'])
def post_question():
    ''' Post an answer function'''
    question_desc = request.get_json('description')['description']
    if not question_desc or question_desc == " ":
        abort(400)
    if not request.json:
        abort(400)
    question = Question(str(question_desc))
    questions.append(question.__dict__)
    return jsonify({'question': questions})

@app.route('/stackoverflowlite/api/v1/questions/<question_id>', methods=['PUT'])
def post_answer(question_id):
    '''Post answer function'''
    question = [question for question in questions if question['question_id'] == question_id]
    if len(question) == 0:
        abort(404)
    answer_desc = request.get_json('answer')['answer']
    if not answer_desc or answer_desc == " ":
        abort(400)
    if not request.json:
        abort(400)
    answer = Answer(str(answer_desc))
    question[0]['answers'].append(answer.__dict__)
    return jsonify({'question': question[0]})


@app.route('/stackoverflowlite/api/v1/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    '''Delete question function'''
    question = [question for question in questions if question['question_id'] == question_id]
    if len(question) == 0:
        abort(404)
    questions.remove(question[0])
    return jsonify({'message': "Deleted successfully"})


@app.route('/stackoverflowlite/api/v1/signup', methods=['POST'])
def sign_up():
    email = request.get_json('email')['email']
    password = request.get_json('password')['password']
    user_email = [user_email for user_email in users if user_email['email'] == email]
    if not email or email == " ":
        abort(400)
    if not re.match(email_format, email):
        return jsonify({"message":"incorrect email format"})
    if not password or password == " ":
        abort(400)
    if not request.json:
        abort(400)
    if user_email:
       abort(409)
    user = User(str(email), str(password))
    users.append(user.__dict__)
    return jsonify({"User": users})



@app.route('/stackoverflowlite/api/v1/login', methods=['POST'])
def login():
    email = request.get_json('email')['email']
    password = request.get_json('password')['password']

    if not email or email == " ":
        abort(400)
    if not re.match(email_format, email):
        return jsonify({"message": "incorrect email format"})
    if not password or password == " ":
        abort(400)
    if not request.json:
        abort(400)
    user_email = [user_email for user_email in users if user_email['email'] == email]
    user_password = [user_password for user_password in users if user_password['password'] == password]

    if not user_email:
        return jsonify({"message": "email is incorrect"})
    elif not user_password:
        return jsonify({"message": "password is incorrect"})
    elif user_email and password:
        return jsonify({"message": "login succesful"})

@app.errorhandler(404)
def not_found(error):
    '''404 Error function'''
    return make_response(jsonify({'error':str(error)}), 404)


@app.errorhandler(400)
def bad_request(error):
    '''400 Error function'''
    return make_response(jsonify({'error':str(error)}), 400)


@app.errorhandler(409)
def bad_request(error):
    '''400 Error function'''
    return make_response(jsonify({'error':str(error)}), 409)