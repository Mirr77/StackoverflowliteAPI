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

    question_desc = request.get_json('description')['description']

    if not question_desc or question_desc == " ":
        response = jsonify({"message": "Question not provided"})
        response.status_code = 400
        return response

    if not request.json:
        response = jsonify({"message": "incorrect format"})
        response.status_code = 400
        return response

    Question(str(question_desc))
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("select * from questions where question_desc = '{}'".format(question_desc))
    questions = cur.fetchall()
    cur.close()
    close_connection(conn)
    return jsonify({'question': questions})


@api.route('/questions/<question_id>', methods=['GET', 'DELETE'])
def get_question(question_id):
    ''' Get a question function '''
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("select * from questions where question_id = {}".format(question_id))
    question = cur.fetchall()
    cur.close()
    close_connection(conn)

    if len(question) == 0:
        response = jsonify({"message": "Question not found"})
        response.status_code = 404
        return response

    if request.method == 'GET':
        return jsonify({'question': question[0]})

    cur.execute("delete from questions where question_id = {}".format(question_id))
    return jsonify({'message': "Deleted successfully"})


@api.route('/questions/<question_id>/answers', methods=['POST'])
def post_answer(question_id):
    '''Post answer function'''
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("select * from questions where question_id = {}".format(question_id))
    question = cur.fetchall()
    cur.close()
    close_connection(conn)

    if len(question) == 0:
        response = jsonify({"message": "Question not found"})
        response.status_code = 400
        return response

    answer_desc = request.get_json('answer')['answer']
    if not answer_desc or answer_desc == " ":
        response = jsonify({"message": "Answer not provided"})
        response.status_code = 400
        return response, response.status_code

    if not request.json:
        response = jsonify({"message": "Incorrect request format"})
        response.status_code = 400
        return response

    Answer(str(answer_desc))
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("select * from answers where answer_desc = '{}'".format(answer_desc))
    answer = cur.fetchall()
    cur.execute("update questions set answers = array_append(answers, '{}')".format(answer[0][1]))
    cur.close()
    close_connection(conn)
    return jsonify({'answer': answer})

