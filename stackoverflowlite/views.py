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
    if not answer or answer_desc == " ":
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

@app.errorhandler(404)
def not_found(error):
    '''404 Error function'''
    return make_response(jsonify({'error':str(error)}), 404)


@app.errorhandler(400)
def bad_request(error):
    '''400 Error function'''
    return make_response(jsonify({'error':str(error)}), 400)