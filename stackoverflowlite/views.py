''' import modules '''
from flask import jsonify, abort, make_response, request
from . import app
from .models.questions import questions, Question

@app.route('/stackoverflowlite/api/v1/questions', methods=['GET'])
def get_questions():
    ''' Get all questions function '''
    return jsonify({'questions': [question for question in questions]})