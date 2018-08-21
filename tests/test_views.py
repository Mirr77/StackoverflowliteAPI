'''import modules'''
import pytest
from flask import json
from stackoverflowlite import APP


@pytest.fixture
def client():
    '''create test client function'''
    test_client = APP.test_client()
    return test_client


def test_index(client):
    '''test index page'''
    response = client.get('/api/v1')
    data = json.loads(response.data)["message"]
    assert data == "Welcome to stackoverflowlite"


def test_get_questions(client):
    '''test get questions endpoint'''
    response = client.get('/api/v1/questions')
    data = json.loads(response.data)["questions"]
    assert type(data) == list


def test_post_question(client):
    '''test post question endpoint'''
    question = {"description": "How to test a post"}
    response = client.post('/api/v1/questions', data=json.dumps(question))
    assert len(json.loads(response.data)["question"]) == 1


def test_get_question(client):
    '''test get a question endpoint'''
    res = client.get('/api/v1/questions')
    question_id = json.loads(res.data)["questions"][0]["question_id"]
    response = client.get('/api/v1/questions/{}'.format(str(question_id)))
    assert json.loads(response.data)["question"]["question_id"] == question_id


def test_post_answer(client):
    '''test post an answer'''
    res = client.get('/api/v1/questions')
    question_id = json.loads(res.data)["questions"][0]["question_id"]
    answer = {"answer": "you use pytest"}
    response = client.post('/api/v1/questions/{}/answers'.format(str(question_id)),
                           content_type='application/json', data=json.dumps(answer))
    assert len(json.loads(response.data)["question"]["answers"]) == 1


def test_delete_question(client):
    '''test delete a question endpoint'''
    res = client.get('/api/v1/questions')
    question_id = json.loads(res.data)["questions"][0]["question_id"]
    response = client.delete('/api/v1/questions/{}'.format(str(question_id)))
    assert b'message' in response.data


def test_no_question(client):
    '''test question not found'''
    res = client.get('/api/v1/questions/1')
    assert res.status_code == 404


def test_empty_question(client):
    '''test empty question provided'''
    question = {"description": " "}
    response = client.post('/api/v1/questions', data=json.dumps(question))
    assert response.status_code == 400


def test_no_question_answer(client):
    '''test no answer provided'''
    res = client.post('/api/v1/questions/1/answers')
    assert res.status_code == 404


def test_no_question_delete(client):
    '''test no question to delete'''
    res = client.delete('/api/v1/questions/1')
    assert res.status_code == 404


def test_signup(client):
    '''test signup endpoint'''
    user = {"email": "mirrmaina@gmail.com", "password": "password"}
    response = client.post('/api/v1/signup', data=json.dumps(user))
    assert len(json.loads(response.data)["User"]) == 1


def test_login(client):
    '''test login endpoint'''
    user = {"email": "mirrmaina@gmail.com", "password": "password"}
    response = client.post('/api/v1/login', data=json.dumps(user))
    assert response.status_code == 200


def test_empty_email_login(client):
    '''test no email provided'''
    user = {"email": " ", "password":"password"}
    response = client.post('/api/v1/login', data=json.dumps(user))
    assert response.status_code == 400


def test_empty_email_signup(client):
    '''test empty email provided'''
    user = {"email": " ", "password": "password"}
    response = client.post('/api/v1/signup', data=json.dumps(user))
    assert response.status_code == 400


def test_empty_password_login(client):
    '''test empty password for login'''
    response = client.post('/api/v1/login',
                           data=dict(email="mirrmaina@gmail,com", password=" "))
    assert response.status_code == 400


def test_empty_password_signup(client):
    '''test empty password for signup'''
    response = client.post('/api/v1/signup',
                           data=dict(email="mirrmaina@gmail,com", password=""))
    assert response.status_code == 400
