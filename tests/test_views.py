from stackoverflowlite import app
from flask import json
import pytest


@pytest.fixture
def client():
    test_client = app.test_client()
    return test_client


def test_index(client):
    response = client.get('/')
    data = json.loads(response.data)["message"]
    assert data == "Welcome to stackoverflowlite"


def test_get_questions(client):
    response = client.get('/questions')
    data = json.loads(response.data)["questions"]
    assert type(data) == list


def test_post_question(client):
    question = {"description": "How to test a post"}
    response = client.post('/questions', data=json.dumps(question))
    assert len(json.loads(response.data)["question"]) == 1


def test_get_question(client):
    res = client.get('/questions')
    question_id = json.loads(res.data)["questions"][0]["question_id"]
    response = client.get('/questions/{}'.format(question_id))
    assert json.loads(response.data)["question"]["question_id"] == question_id


def test_post_answer(client):
    res = client.get('/api/v1/questions')
    question_id = json.loads(res.data)["questions"][0]["question_id"]
    answer = {"answer":"you use pytest"}
    response = client.post('/questions/{}/answers'.format(question_id),
                          content_type='application/json',
                          data=json.dumps(answer))
    assert len(json.loads(response.data)["question"]["answers"]) == 1


def test_delete_question(client):
    res = client.get('/api/v1/questions')
    question_id = json.loads(res.data)["questions"][0]["question_id"]
    response = client.delete('/questions/{}'.format(question_id))
    assert b'message' in response.data


def test_no_question(client):
    res = client.get('/api/v1/questions/1')
    assert res.status_code == 404


def test_empty_question(client):
    question = {"description": " "}
    response = client.post('/questions', data=json.dumps(question))
    assert response.status_code == 400


def test_no_question_answer(client):
    res = client.put('/questions/1')
    assert res.status_code == 404


def test_no_question_delete(client):
    res = client.delete('/questions/1')
    assert res.status_code == 404


def test_signup(client):
    user = {"email": "mirrmaina@gmail.com","password":"password"}
    response = client.post('/signup', data=json.dumps(user))
    assert len(json.loads(response.data)["User"]) == 1


def test_login(client):
    user = {"email": "mirrmaina@gmail.com", "password": "password"}
    response = client.post('/login', data=json.dumps(user))
    assert response.status_code == 200


def test_empty_email_login(client):
    user = {"email": " ", "password":"password"}
    response = client.post('/api/v1/login', data=json.dumps(user))
    assert response.status_code == 400


def test_empty_email_signup(client):
    user = {"email": " ", "password":"password"}
    response = client.post('/signup', data=json.dumps(user))
    assert response.status_code == 400


def test_empty_password_login(client):
    user = {"password": " ", "email": "mirrmaina@gmail,com" }
    response = client.post('/login', data=dict(email="mirrmaina@gmail,com", password=" "))
    assert response.status_code == 400


def test_empty_password_signup(client):
    user = {"password": " ", "email": "mirrmaina@gmail,com"}
    response = client.post('/signup', data=dict(email="mirrmaina@gmail,com", password=""))
    assert response.status_code == 400
 

