from stackoverflowlite import app
from flask import json
import pytest


@pytest.fixture
def client():
    test_client = app.test_client()
    return test_client

def test_get_questions(client):
    response = client.get('/stackoverflowlite/api/v1/questions')
    data = json.loads(response.data)["questions"]
    assert type(data) == list

def test_post_question(client):
    question = {"description": "How to test a post"}
    response = client.post('/stackoverflowlite/api/v1/questions', data=json.dumps(question))
    assert len(json.loads(response.data)["question"]) == 1


def test_get_question(client):
    res = client.get('/stackoverflowlite/api/v1/questions')
    question_id = json.loads(res.data)["questions"][0]["question_id"]
    response = client.get('/stackoverflowlite/api/v1/questions/{}'.format(str(question_id)))
    assert json.loads(response.data)["question"]["question_id"] == question_id
