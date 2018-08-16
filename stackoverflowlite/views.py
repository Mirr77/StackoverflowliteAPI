''' import modules '''
from flask import jsonify, abort, make_response, request
from . import app
from .models.questions import questions, Question, Answer
from .models.users import User, users


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
    question = Question(str(question_desc))
    questions.append(question.__dict__)
    return jsonify({'question': questions})