''' import modules'''
from uuid import uuid4
from db.dbconfig import open_connection,close_connection


class Question(object):

    ''' Question Model '''
    def __init__(self, question_desc):
        self.question_id = str(uuid4())
        self.question_desc = question_desc
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("insert into questions(question_desc) values('{}')".format(question_desc))
        cur.close()
        close_connection(conn)


class Answer(object):
    ''' Answer Model '''

    def __init__(self, answer_desc):
        self.answer_id = str(uuid4())
        self.answer_desc = answer_desc
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("insert into answers(answer_desc) values('{}')".format(answer_desc))
        close_connection(conn)
