''' import modules '''
from flask import jsonify, request
from stackoverflowlite.views import api
from stackoverflowlite.models.questions import Question, Answer
from db.dbconfig import open_connection, close_connection
from stackoverflowlite.utils.util_func import requires_auth

email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"


@api.route('/')
@requires_auth
def index(identity):
    return jsonify({'message': 'Welcome to stackoverflowlite API'})


@api.route('/questions', methods=['GET', 'POST'])
@requires_auth
def questions(identity):
    conn = open_connection()
    cur = conn.cursor()

    ''' Get all questions function '''
    if request.method == 'GET':
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("select * from questions")
        questions = cur.fetchall()
        return jsonify({'questions': [question for question in questions]})

    else:
        question_desc = request.get_json('description')['description']

        if not question_desc or question_desc == " ":
            response = jsonify({"message": "Question not provided"})
            response.status_code = 400
            return response

        if not request.json:
            response = jsonify({"message": "incorrect format"})
            response.status_code = 400
            return response

        cur.execute("select * from questions where question_desc='{}' and user_id={}"
                                        .format(question_desc, identity))
        question_exists = cur.fetchall()

        if len(question_exists) > 0:
            response = jsonify({"message": "That question exists"})
            response.status_code = 409
            return response

        Question(str(question_desc))
        cur.execute("select question_id from questions where question_desc = '{}'".format(question_desc))
        question_id = cur.fetchone()
        cur.execute("update questions set user_id = {} where question_id = {}"
                    .format(identity, question_id[0]))
        cur.execute("select * from questions where question_desc = '{}' and user_id = {}"
                    .format(question_desc, identity))
        question = cur.fetchall()
        cur.execute("update users set questions = array_append(questions, '{}')".format(question[0][1]))
        cur.close()
        close_connection(conn)
        return jsonify({'question': question})


@api.route('/questions/<question_id>', methods=['GET', 'DELETE'])
@requires_auth
def get_question(identity, question_id):
    ''' Get a question function '''
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("select * from questions where question_id = {}".format(question_id))
    question = cur.fetchall()

    if len(question) == 0:
        response = jsonify({"message": "Question not found"})
        response.status_code = 404
        return response

    if request.method == 'GET':
        return jsonify({'question': question[0]})

    if question[0][2] != identity:
        response = jsonify({"message": "You don't have access rights to delete that question"})
        response.status_code = 400
        return response

    cur.execute("delete from questions where question_id = {} and user_id = {}".format(question_id, identity))
    cur.close()
    close_connection(conn)
    return jsonify({'message': "Deleted successfully"})


@api.route('/questions/<question_id>/answers', methods=['POST'])
@requires_auth
def post_answer(identity, question_id):
    '''Post answer function'''
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("select * from questions where question_id = {}".format(question_id))
    question = cur.fetchall()

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

    cur.execute("select * from answers where question_id={} and user_id={}"
                .format(question_id, identity))
    answer_exists = cur.fetchall()
    if answer_exists:
        response = jsonify({"message": " You have already provided that answer"})
        response.status_code = 409
        return response

    Answer(str(answer_desc))
    cur.execute("select id from answers where answer_desc = '{}'".format(answer_desc))
    answer_id = cur.fetchone()
    cur.execute("update answers set user_id = {} where id = '{}'".format(identity, answer_id[0]))
    cur.execute("select * from answers where answer_desc = '{}' and user_id={}".format(answer_desc, identity))
    answer = cur.fetchone()
    cur.execute("update questions set answers = array_append(answers, '{}')".format(answer[1]))
    cur.close()
    close_connection(conn)
    return jsonify({'answer': answer})


@api.route('/user_questions', methods=['GET'])
@requires_auth
def get_user_questions(identity):
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("select questions from users where user_id = {}".format(identity))
    questions = cur.fetchone()
    response = jsonify({"questions": questions[0]})
    response.status_code = 200
    close_connection(conn)
    return response


@api.route('/question_answers/<question_id>', methods=['GET'])
@requires_auth
def get_question_answers(identity,question_id):
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("select answers from questions where question_id = {}".format(question_id))
    answers = cur.fetchone()
    response = jsonify({"answers": answers[0]})
    response.status_code = 200
    return response




