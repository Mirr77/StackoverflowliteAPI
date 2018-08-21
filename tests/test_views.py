from stackoverflowlite import app
from flask import json
import pytest


@pytest.fixture
def client():
    test_client = app.test_client()
    return test_client


def test_index(client):
    response = client.get('api/v1/')
    data = json.loads(response.data)["message"]
    assert data == "Welcome to stackoverflowlite API"


def test_get_questions(client):
    response = client.get('api/v1/questions')
    data = json.loads(response.data)["questions"]
    assert type(data) == list


def test_post_question(client):
    question = {"description": "How to test a post"}
    response = client.post('api/v1/questions', data=json.dumps(question))
    assert len(json.loads(response.data)["question"]) == 1


def test_get_question(client):
    res = client.get('api/v1/questions')
    question_id = json.loads(res.data)["questions"][0][0]
    response = client.get('api/v1/questions/{}'.format(question_id))
    assert json.loads(response.data)["question"][0] == question_id


def test_post_answer(client):
    res = client.get('/api/v1/questions')
    question_id = json.loads(res.data)["questions"][0][0]
    answer = {"answer":"you use pycharm"}
    response = client.post('/questions/{}/answers'.format(question_id),
                          content_type='application/json',
                          data=json.dumps(answer))
    assert len(json.loads(response.data)["question"][4]) == 1


def test_delete_question(client):
    res = client.get('/api/v1/questions')
    question_id = json.loads(res.data)["questions"][0][0]
    response = client.delete('api/v1/questions/{}'.format(question_id))
    assert b'message' in response.data


def test_no_question(client):
    res = client.get('/api/v1/questions/1')
    assert res.status_code == 404


def test_empty_question(client):
    question = {"description": " "}
    response = client.post('api/v1/questions', data=json.dumps(question))
    assert response.status_code == 400


def test_no_question_answer(client):
    res = client.put('/questions/1')
    assert res.status_code == 404


def test_no_question_delete(client):
    res = client.delete('api/v1/questions/1')
    assert res.status_code == 404

