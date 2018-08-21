from dbconfig import open_connection, close_connection

QUERIES = [
  """
  CREATE TABLE IF NOT EXISTS users(
          user_id SERIAL PRIMARY KEY NOT NULL,
          username VARCHAR NOT NULL,
          email VARCHAR NOT NULL,
          password VARCHAR NOT NULL
          )
  """,

  """
  CREATE TABLE IF NOT EXISTS questions(
          question_id SERIAL PRIMARY KEY NOT NULL,
          question_desc VARCHAR NOT NULL,
          user_id INT REFERENCES users(user_id)
          )
  """,

  """
  CREATE TABLE IF NOT EXISTS answers(
          id SERIAL PRIMARY KEY NOT NULL,
          answer_desc VARCHAR NOT NULL,
          question_id INT REFERENCES questions(question_id),
          user_id INT REFERENCES users(user_id)
        
          )
  """
]

def create_tables():
    """ Create main app tables """
    conn = open_connection()
    cur = conn.cursor()

    for query in QUERIES:
        cur.execute(query)

    close_connection(conn)



