from db.dbconfig import open_connection, close_connection


class Blacklist(object):
    ''' Model for blacklisted tokens '''

    def __init__(self, token):
        ''' Initialize token blacklist '''
        self.token = token

        conn = open_connection()
        cur = conn.cursor()
        cur.execute("insert into blacklist(token) values('{}')".format(token))
        cur.close()
        close_connection(conn)
