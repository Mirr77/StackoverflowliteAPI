
from uuid import uuid4
users = []


class User(object):
    ''' User model '''
    def __init__(self, email, password):
        ''' Initialize user '''
        self.user_id = str(uuid4())
        self.email = email
        self.password = password
        self.questions = []

    def __repr__(self):
        return 'User: {}'.format(self.email)