import psycopg2
conn = conn = psycopg2.connect("dbname='stackoverflowlite' user='postgres' host='localhost' password='password'")
cur = conn.cursor()


class Blacklist(object):
    '''model for blacklisted tokens'''
    cur.execute("create table blacklist(token_id serial primary key not null,token varchar(500) not null")
    conn.commit()

    def __init__(self, token):
        ''' Initialize token blacklist '''
        self.token = token

