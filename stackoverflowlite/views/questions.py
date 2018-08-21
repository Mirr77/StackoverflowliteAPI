''' import modules '''
from flask import jsonify, request
from stackoverflowlite.views import api
from stackoverflowlite.models.questions import Question, Answer
from db.dbconfig import open_connection, close_connection

email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"


@api.route('/')
def index():
    return jsonify({'message': 'Welcome to stackoverflowlite API'})


@api.route('/questions', methods=['GET', 'POST'])
def questions():
    ''' Get all questions function '''
    if request.method == 'GET':
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("select * from questions")
        questions = cur.fetchall()
        cur.close()
        close_connection(conn)
        return jsonify({'questions': [question for question in questions]})

