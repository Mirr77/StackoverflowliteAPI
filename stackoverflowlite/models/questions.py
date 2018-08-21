''' import modules'''
from uuid import uuid4

QUESTIONS = []


class Question(object):

    ''' Question Model '''
    def __init__(self, question_desc):
        self.question_id = str(uuid4())
        self.question_desc = question_desc
        self.answers = []

    def __repr__(self):
        return 'Description: {}'.format(self.question_desc)


class Answer(object):
    ''' Answer Model '''

    def __init__(self, answer_desc):
        self.answer_id = str(uuid4())
        self.answer_desc = answer_desc

    def __repr__(self):
        return 'Answer: {}'.format(self.answer_desc)
