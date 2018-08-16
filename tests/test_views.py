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
