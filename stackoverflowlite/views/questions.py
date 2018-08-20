''' import modules '''
from flask import jsonify, request
from stackoverflowlite.views import api
from stackoverflowlite.models.questions import Question, Answer, cur, conn
email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"


@api.route('/questions', methods=['GET', 'POST'])
def questions():
    ''' Get all questions function '''
    if request.method == 'GET':
        cur.execute("select * from questions")
        questions = cur.fetchall()
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
    cur.execute("select * from questions where question_desc = '{}'".format(question_desc))
    questions = cur.fetchall()
    return jsonify({'question': questions})


@api.route('/questions/<question_id>', methods=['GET', 'DELETE'])
def get_question(question_id):
    ''' Get a question function '''
    cur.execute("select * from questions where question_id = {}".format(question_id))
    question = cur.fetchall()

    if len(question) == 0:
        response = jsonify({"message": "Question not found"})
        response.status_code = 404
        return response

    if request.method == 'GET':
        return jsonify({'question': question[0]})

    cur.execute("delete from questions where question_id = {}".format(question_id))
    return jsonify({'message': "Deleted successfully"})


@api.route('/questions/<question_id>', methods=['PUT'])
def post_answer(question_id):
    '''Post answer function'''
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

    Answer(str(answer_desc))
    cur.execute("select * from answers where answer_desc = '{}'".format(answer_desc))
    answer = cur.fetchall()
    print(answer)
    cur.execute("update questions set answers = array_append(answers, '{}')".format(answer[0][1]))
    conn.commit()
    return jsonify({'answer': answer})

